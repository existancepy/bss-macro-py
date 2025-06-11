import ctypes
import platform

def check_screen_recording_permission():
    if platform.system() != "Darwin":
        raise RuntimeError("This function is macOS only.")

    try:
        # Load CoreGraphics framework
        cg = ctypes.cdll.LoadLibrary("/System/Library/Frameworks/CoreGraphics.framework/CoreGraphics")

        # Declare return type of the function
        cg.CGPreflightScreenCaptureAccess.restype = ctypes.c_bool

        has_access = cg.CGPreflightScreenCaptureAccess()
        return cg.CGPreflightScreenCaptureAccess()

    except Exception as e:
        print("Error checking screen recording permission:", e)
        return False

print("Screen Recording Permission:", check_screen_recording_permission())
