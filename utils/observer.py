from kivy.utils import platform
import os
import time

# For PC monitoring
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    Observer = None
    FileSystemEventHandler = object

# Only import jnius and Android-specific libs if on Android
if platform == 'android':
    try:
        from jnius import autoclass, PythonJavaClass, java_method
        from android.permissions import request_permissions, Permission
        
        # Android classes
        Context = autoclass('android.content.Context')
        FileObserver = autoclass('android.os.FileObserver')
        
    except Exception as e:
        print(f"Failed to load Android libraries even though on Android: {e}")
        platform = 'pc' 

class ImageEventHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback

    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            print(f"New image detected by watchdog: {event.src_path}")
            self.callback(event.src_path)

def start_listening(callback):
    """Starts monitoring for new images in Downloads/WhatsApp folders."""
    if platform == 'android':
        # On Android, we will monitor common directories
        # This is a simplified version; real implementation uses PythonJavaClass
        print("Starting Android FileObservers...")
        # (Full Android FileObserver implementation would go here for buildozer)
    else:
        if Observer:
            # Common download paths for simulation
            paths_to_watch = [
                os.path.join(os.path.expanduser("~"), "Downloads"),
                os.path.join(os.getcwd(), "test_downloads")
            ]
            
            # Create test_downloads if doesn't exist for simulation
            if not os.path.exists("test_downloads"):
                os.makedirs("test_downloads")

            observer = Observer()
            event_handler = ImageEventHandler(callback)
            
            for path in paths_to_watch:
                if os.path.exists(path):
                    observer.schedule(event_handler, path, recursive=False)
                    print(f"Monitoring folder: {path}")
            
            observer.start()
            return observer
        else:
            print("Watchdog not installed. Cannot monitor files on PC.")
    return None

def trigger_notification(title, message):
    """Triggers a system notification."""
    if platform == 'android':
        # (Actual implementation using Android's NotificationManager)
        print(f"Android Notif: {title} - {message}")
    else:
        # PC Notification simulation (could use plyer but avoiding extra dependencies)
        print(f"--- NOTIFICATION ---")
        print(f"Title: {title}")
        print(f"Message: {message}")
        print(f"--------------------")
