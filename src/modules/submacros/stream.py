from flask import Flask, Response, render_template_string
import cv2
import numpy as np
import mss
import mss.darwin
mss.darwin.IMAGE_OPTIONS = 0
import threading
import subprocess
import time
import re
import os
import gc
import sys
from collections import deque
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


class cloudflaredStream:
    def __init__(self):
        self.app = Flask(__name__)
        self.streaming = False
        self.serverThread = None
        self.publicURL = None
        self.cfProc = None
        self.target_fps = 60
        self.last_frame_time = 0
        self.frame_count = 0
        self.restart_count = 0
        
        self.frame_buffer = None
        self.frame_lock = threading.Lock()
        self.frame_ready = threading.Event()
        self.capture_thread = None
        
        self.fps_history = deque(maxlen=60)
        self.last_fps_check = time.time()
        self.current_fps = 0
        
        self.resolution = 1.0
        self.jpeg_quality = 60 
        self.adaptive_quality = True

 
        self.HTML_PAGE = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Live Screen Stream</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {
                    background-color: #121212;
                    color: #ffffff;
                    font-family: 'Segoe UI', sans-serif;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }
                h1 {
                    margin-top: 20px;
                    font-size: 2rem;
                }
                .video-container {
                    margin-top: 20px;
                    width: 90%;
                    max-width: 960px;
                    border-radius: 10px;
                    overflow: hidden;
                    position: relative;
                }
                img {
                    width: 100%;
                    height: auto;
                    display: block;
                    border-radius: 10px;
                }
                .stats {
                    position: absolute;
                    top: 10px;
                    right: 10px;
                    background-color: rgba(0,0,0,0.6);
                    padding: 5px 10px;
                    border-radius: 5px;
                    font-size: 0.8rem;
                    font-family: monospace;
                }
                @media (max-width: 600px) {
                    h1 { font-size: 1.5rem; }
                }
                #fps-counter {
                    color: #4CAF50;
                    font-weight: bold;
                }
                .refresh-btn {
                    margin-top: 10px;
                    padding: 8px 16px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                }
                .refresh-btn:hover {
                    background-color: #45a049;
                }
            </style>
            <script>
                // JavaScript for auto-reconnect and FPS display
                document.addEventListener('DOMContentLoaded', function() {
                    const img = document.querySelector('.video-container img');
                    const fpsCounter = document.getElementById('fps-counter');
                    let errorCount = 0;
                    
                    if (img) {
                        img.onerror = function() {
                            errorCount++;
                            if (errorCount > 3) {
                                console.log("Stream error detected, reconnecting...");
                                setTimeout(() => {
                                    img.src = "/video_feed?t=" + new Date().getTime();
                                    errorCount = 0;
                                }, 1000);
                            }
                        };
                        
                        // Check stream health periodically
                        setInterval(() => {
                            fetch('/fps')
                                .then(response => response.json())
                                .then(data => {
                                    fpsCounter.textContent = data.fps.toFixed(1);
                                    fpsCounter.style.color = data.fps > 30 ? '#4CAF50' : 
                                                            (data.fps > 15 ? '#FFC107' : '#F44336');
                                })
                                .catch(err => console.log('Error fetching FPS data'));
                        }, 1000);
                    }
                    
                    document.getElementById('refresh-stream').addEventListener('click', function() {
                        if (img) {
                            img.src = "/video_feed?t=" + new Date().getTime();
                        }
                    });
                });
            </script>
        </head>
        <body>
            <h1>Existance Macro Live Stream</h1>
            <div class="video-container">
                {% if streaming %}
                    <img src="/video_feed" alt="Live Stream">
                    <div class="stats">FPS: <span id="fps-counter">0.0</span></div>
                {% else %}
                    <p style="text-align:center; font-size:1.2rem;">🔘 Macro Stopped</p>
                {% endif %}
            </div>
            {% if streaming %}
            <button id="refresh-stream" class="refresh-btn">Refresh Stream</button>
            {% endif %}
        </body>
        </html>
        """

        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/video_feed', 'video_feed', self.videoFeed)
        self.app.add_url_rule('/fps', 'fps', self.get_fps, methods=['GET'])
        
        #enable garbage collection
        gc.enable()
        gc.set_threshold(700, 10, 5)

        #get the cloudflared path
        paths = [
            "cloudflared",
            "/opt/homebrew/bin/cloudflared",
            "/usr/local/Homebrew/bin/cloudflared"
        ]
        for path in paths:
            if os.path.isfile(path) and os.access(path, os.X_OK):
                self.cloudflaredPath = path
                break
        else:
            self.cloudflaredPath = None

    def index(self):
        return render_template_string(self.HTML_PAGE, streaming=self.streaming)

    def get_fps(self):
        """API endpoint to report current FPS"""
        from flask import jsonify
        return jsonify({'fps': self.current_fps})

    def videoFeed(self):
        if not self.streaming:
            return "", 204
        return Response(self._generate_frames_with_restart(), 
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    
    def update_fps(self):

        now = time.time()
        self.fps_history.append(now)
        
        # Calculate FPS over recent history
        if len(self.fps_history) >= 10:
            time_diff = self.fps_history[-1] - self.fps_history[0]
            if time_diff > 0:  # Avoid division by zero
                self.current_fps = (len(self.fps_history) - 1) / time_diff
        
        # Adjust quality if enabled and we have enough data
        if self.adaptive_quality and len(self.fps_history) >= 30:
            self._adjust_quality()
    
    def _adjust_quality(self):

        if self.current_fps < 30:
            if self.jpeg_quality > 40:
                self.jpeg_quality -= 5
                
            elif self.resolution > 0.5:
                self.resolution -= 0.1

        elif self.current_fps > 55:
            if self.resolution < 1.0:
                self.resolution += 0.1
                self.resolution = min(1.0, self.resolution)
            elif self.jpeg_quality < 80:
                self.jpeg_quality += 5
    
    def _generate_frames_with_restart(self):
        max_restarts = 5
        restart_count = 0
        
        while self.streaming and restart_count < max_restarts:
            try:
                yield from self.generateFrames()
                #generator exited normally
                time.sleep(0.5)
                restart_count += 1
                print(f"Restarting frame generator (attempt {restart_count}/{max_restarts})")
            except Exception as e:
                print(f"Frame generation error: {e}. Restarting capture...")
                time.sleep(0.5)  # Brief pause before restart
                restart_count += 1
                self.restart_count += 1
        
        print("Max restarts reached or streaming stopped.")

    def start_capture_thread(self):
        if self.capture_thread is None or not self.capture_thread.is_alive():
            self.capture_thread = threading.Thread(target=self._capture_screen, daemon=True)
            self.capture_thread.start()
            print("Capture thread started")
    
    def _capture_screen(self):
        # Optimize process priority on macOS
        if sys.platform == 'darwin':
            try:
                os.system('renice -n -20 -p ' + str(os.getpid()))
            except:
                pass
        
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            
            while self.streaming:
                try:
                    screen = np.array(sct.grab(monitor), dtype=np.uint8)
                    
                    #resolution scaling if needed
                    if self.resolution < 1.0:
                        h, w = screen.shape[:2]
                        new_h, new_w = int(h * self.resolution), int(w * self.resolution)
                        screen = cv2.resize(screen, (new_w, new_h), interpolation=cv2.INTER_NEAREST)
                    
                    #drop alpha channel
                    screen = screen[:, :, :3]

                    with self.frame_lock:
                        self.frame_buffer = screen
                        self.frame_ready.set()
                        
                except Exception as e:
                    print(f"Capture error: {e}")
                
                #120 captures per second
                time.sleep(1/120)

    def generateFrames(self):
        self.start_capture_thread()
        
        #timing variables
        frame_interval = 1.0 / self.target_fps
        last_gc_time = time.time()
        start_time = time.time()
        frames_since_gc = 0
        
        #JPEG encoding parameters
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), self.jpeg_quality,
                       int(cv2.IMWRITE_JPEG_OPTIMIZE), 1]
        
        #restart after 30 seconds to prevent degradation
        max_run_time = 30  # seconds
        
        # Frame tracking
        self.frame_count = 0
        self.fps_history.clear()
        
        while self.streaming:
            if time.time() - start_time > max_run_time:
                print("Periodic capture restart for performance")
                break
            
            current_time = time.time()
            elapsed = current_time - self.last_frame_time
            
            if elapsed < frame_interval:
                sleep_time = frame_interval - elapsed
                if sleep_time > 0.001:
                    time.sleep(sleep_time - 0.001)  #slightly less to account for processing
                continue
            
            #wait for a frame to be ready
            if not self.frame_ready.is_set():
                self.frame_ready.wait(timeout=0.5)
                if not self.frame_ready.is_set():
                    continue
            
            #get the latest frame
            with self.frame_lock:
                if self.frame_buffer is None:
                    continue
                
                frame = self.frame_buffer.copy()
                self.frame_ready.clear()
            
            try:
                #update timing and counters
                self.last_frame_time = time.time()
                self.frame_count += 1
                frames_since_gc += 1
                
                #update FPS calculation
                self.update_fps()
                
                #encode frame
                ret, buffer = cv2.imencode('.jpg', frame, encode_param)
                
                if not ret:
                    continue
                
                #yield frame
                frame_data = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')
                
                frame = None
                buffer = None
                frame_data = None
                
                #garbage collection
                if frames_since_gc >= 180:
                    gc.collect()
                    frames_since_gc = 0
                
            except Exception as e:
                print(f"Frame processing error: {e}")
                # Force cleanup
                gc.collect()
                time.sleep(0.1)
            
            time.sleep(0.0001)

    def _run_server(self):
        #use the production WSGI server if available
        try:
            # from waitress import serve
            # print("Starting server with Waitress WSGI server")
            # serve(self.app, host='0.0.0.0', port=8081, threads=4)
            raise ImportError
        except ImportError:
            # Fall back to Werkzeug server
            from werkzeug.serving import run_simple
            print("Starting server with Werkzeug (install waitress for better performance)")
            run_simple('0.0.0.0', 8081, self.app, threaded=True, use_reloader=False)
    
    def isCloudflaredInstalled(self):
        return self.cloudflaredPath
    
        try:
            result = subprocess.run(
                [self.getCloudflaredPath(), "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode == 0:
                return True
        except FileNotFoundError:
            return False

    def _run_cloudflared(self):
        time.sleep(2)
        print("Launching Cloudflare tunnel")
        self.cfProc = subprocess.Popen(
            [self.cloudflaredPath, "tunnel", "--url", "http://localhost:8081"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        #extract the cloudflare link
        for line in self.cfProc.stdout:
            if "trycloudflare.com" in line and "https://" in line:
                match = re.search(r"https://[a-zA-Z0-9\-]+\.trycloudflare\.com", line)
                if match:
                    url = match.group()
                    print("Cloudflare URL:", url)
                    self.publicURL = url
                    # Write stream URL to file for Discord bot
                    try:
                        import os
                        stream_url_file = os.path.join(os.path.dirname(__file__), '..', '..', 'stream_url.txt')
                        with open(stream_url_file, 'w') as f:
                            f.write(url)
                    except Exception as e:
                        print(f"Failed to write stream URL to file: {e}")
                    break

    def start(self, resolution=1.0):
        self.resolution = resolution
        self.streaming = True
        self.restart_count = 0

        #start the server thread if not already running
        if not self.serverThread or not self.serverThread.is_alive():
            self.serverThread = threading.Thread(target=self._run_server, daemon=True)
            self.serverThread.start()
            print(f"Stream started on http://localhost:8081 (Target: {self.target_fps} FPS)")
            
        #start the Cloudflare tunnel
        threading.Thread(target=self._run_cloudflared, daemon=True).start()

    def stop(self):

        if self.streaming:
            print("Stream stopped.")
        self.streaming = False
        self.publicURL = None

        # Clear stream URL file
        try:
            stream_url_file = os.path.join(os.path.dirname(__file__), '..', '..', 'stream_url.txt')
            if os.path.exists(stream_url_file):
                os.remove(stream_url_file)
        except Exception as e:
            print(f"Failed to remove stream URL file: {e}")
        
        #stop the capture thread
        if self.capture_thread and self.capture_thread.is_alive():
            self.capture_thread.join(timeout=1.0)
        
        #stop Cloudflare tunnel
        if self.cfProc:
            self.cfProc.terminate()
            self.cfProc.wait()
            self.cfProc = None
        
        #clear frame buffer
        with self.frame_lock:
            self.frame_buffer = None
            self.frame_ready.clear()

    def get_stats(self):
        #return current streaming statistics
        return {
            "fps": self.current_fps,
            "resolution": self.resolution,
            "quality": self.jpeg_quality,
            "frames_captured": self.frame_count,
            "restarts": self.restart_count,
            "url": self.publicURL
        }
