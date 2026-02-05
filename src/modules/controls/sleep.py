#custom sleep function with pause support
import time

# Module-level reference to the run state (multiprocessing.Value)
_run_state = None

def set_run_state(run):
    """Set the shared run state for pause checking"""
    global _run_state
    _run_state = run

def is_paused():
    """Check if macro is currently paused (state 5 or 6)"""
    if _run_state is None:
        return False
    return _run_state.value in [5, 6]

def is_stopped():
    """Check if macro stop was requested (state 0)"""
    if _run_state is None:
        return False
    return _run_state.value == 0

def wait_while_paused():
    """Wait while the macro is paused, return True if stop was requested"""
    while is_paused():
        time.sleep(0.1)
    return is_stopped()

def sleep(duration, get_now=time.perf_counter):
    """Pause-aware sleep function"""
    # Check for pause before sleeping
    if wait_while_paused():
        return  # Stop was requested
    
    now = get_now()
    end = now + duration
    while now < end:
        # Periodically check for pause during long sleeps
        if duration > 0.1 and is_paused():
            if wait_while_paused():
                return  # Stop was requested
        now = get_now()

def high_precision_sleep(duration):
    """Pause-aware high precision sleep"""
    # Check for pause before sleeping
    if wait_while_paused():
        return  # Stop was requested
    
    start_time = time.perf_counter()
    while True:
        elapsed_time = time.perf_counter() - start_time
        remaining_time = duration - elapsed_time
        if remaining_time <= 0:
            break
        if remaining_time > 0.02:  # Sleep for 5ms if remaining time is greater
            time.sleep(max(remaining_time/2, 0.0001))  # Sleep for the remaining time or minimum sleep interval
        else:
            pass
        # Check for pause during sleep
        if is_paused():
            if wait_while_paused():
                return  # Stop was requested

def pauseable_sleep(duration):
    """A time.sleep replacement that respects pause state"""
    # Check for pause before sleeping
    if wait_while_paused():
        return  # Stop was requested
    
    # For short sleeps, just sleep normally
    if duration <= 0.2:
        time.sleep(duration)
        return
    
    # For longer sleeps, check for pause periodically
    start = time.perf_counter()
    while time.perf_counter() - start < duration:
        # Sleep in small chunks
        remaining = duration - (time.perf_counter() - start)
        chunk = min(0.1, remaining)
        if chunk > 0:
            time.sleep(chunk)
        # Check for pause
        if is_paused():
            if wait_while_paused():
                return  # Stop was requested