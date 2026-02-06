import time
import os
from engine.steganalysis import check_stego
from utils.observer import start_listening, trigger_notification

# Kivy service imports (only available on Android)
try:
    from jnius import autoclass
    # Communication between app and service
    # We could use OSC or just a shared file/preference
except ImportError:
    pass

def on_new_image(path):
    print(f"Service: New image detected: {path}")
    is_stego = check_stego(path)
    
    basename = os.path.basename(path)
    if is_stego:
        print(f"Service: ALERT! Stego found in {basename}")
        trigger_notification(
            "Security Alert",
            f"Hidden info found in {basename}!"
        )
        # In a real app, we might move the file or log it for the UI
    else:
        print(f"Service: {basename} is clean.")

if __name__ == '__main__':
    print("SteganoScan Service Started.")
    
    # Start the observer
    observer = start_listening(on_new_image)
    
    # Keep the service alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        if observer:
            observer.stop()
            observer.join()
