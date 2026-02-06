import os
import threading
import sys

# Attempt to import Kivy, handle missing module gracefully
try:
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.label import Label
    from kivy.uix.button import Button
    from kivy.uix.scrollview import ScrollView
    from kivy.uix.popup import Popup
    from kivy.clock import Clock
    from kivy.utils import platform
except ImportError:
    print("WARNING: Kivy not found. UI will not be available.")
    print("Please install Kivy using: pip install kivy")
    # Simulation/CLI mode fallback
    platform = 'pc'
    class App:
        def run(self): pass

# Import custom modules
try:
    from engine.steganalysis import check_stego
    from utils.observer import start_listening, trigger_notification
except ImportError as e:
    print(f"Import Error: {e}")
    def check_stego(path): return False
    def start_listening(cb): return None
    def trigger_notification(t, m): print(f"NOTIF: {t} - {m}")

class StegoApp(App):
    def build(self):
        self.title = "SteganoScan Sentinel"
        
        # Root Layout
        self.root = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Header
        self.header = Label(
            text="[b]SteganoScan Sentinel[/b]",
            markup=True,
            font_size='24sp',
            size_hint_y=None,
            height=50
        )
        self.root.add_widget(self.header)
        
        # Status Label
        self.status_label = Label(
            text="Service Status: Initializing...",
            color=(0.2, 0.8, 0.2, 1)
        )
        self.root.add_widget(self.status_label)
        
        # Log View
        self.scroll = ScrollView()
        self.log_text = Label(
            text="App Started.\n",
            size_hint_y=None,
            valign='top',
            halign='left',
            markup=True
        )
        self.log_text.bind(texture_size=self.log_text.setter('size'))
        self.scroll.add_widget(self.log_text)
        self.root.add_widget(self.scroll)
        
        # Bottom Buttons
        btn_layout = BoxLayout(size_hint_y=None, height=100, spacing=10)
        
        # Start Service Button
        self.service_btn = Button(
            text="Start Service",
            background_color=(0.2, 0.6, 0.2, 1)
        )
        self.service_btn.bind(on_release=self.start_sentinel_service)
        btn_layout.add_widget(self.service_btn)
        
        # Test Alert Button
        self.test_btn = Button(
            text="Test Alert UI",
            background_color=(0.8, 0.2, 0.2, 1)
        )
        self.test_btn.bind(on_release=lambda x: self.show_alert_popup("test_image.jpg"))
        btn_layout.add_widget(self.test_btn)
        
        self.root.add_widget(btn_layout)

        # Initialize observer for simulation/immediate feedback
        self.observer = start_listening(self.on_media_changed)
        if self.observer:
            self.add_log("[color=00ff00]Local File Observer Active.[/color]")
        
        return self.root

    def start_sentinel_service(self, instance=None):
        """Starts the background service on Android."""
        if platform == 'android':
            try:
                from android import python_act
                from jnius import autoclass
                service = autoclass('org.cyberwarlab.steganoscan.ServiceSentinelservice')
                mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
                service.start(mActivity, "")
                self.add_log("[color=00ff00]Android Service Started Successfully.[/color]")
                self.status_label.text = "Service Status: Running in Background"
            except Exception as e:
                self.add_log(f"[color=ff0000]Service Error: {e}[/color]")
        else:
            self.add_log("[color=ffff00]Background services are Android-only. Local observer is running.[/color]")

    def on_media_changed(self, path):
        """Callback triggered by the observer."""
        self.add_log(f"New image detected: {os.path.basename(path)}")
        self.run_scan(path)

    def run_scan(self, path):
        """Launches the scan in a thread to keep UI smooth."""
        def scan_thread():
            is_stego = check_stego(path)
            Clock.schedule_once(lambda dt: self.handle_scan_result(path, is_stego))

        threading.Thread(target=scan_thread).start()

    def handle_scan_result(self, path, is_stego):
        """Processes the result of a scan."""
        basename = os.path.basename(path)
        if is_stego:
            self.add_log(f"[color=ff0000]ALERT: Steganography detected in {basename}[/color]")
            trigger_notification(
                "Steganography Detected!",
                f"Suspicious patterns found in {basename}"
            )
            self.show_alert_popup(basename)
        else:
            self.add_log(f"Scan Clean: {basename}")

    def add_log(self, message):
        """Thread-safe way to add logs to the UI."""
        if 'Clock' in globals():
            def update_log(dt):
                self.log_text.text += f"{message}\n"
            Clock.schedule_once(update_log)
        else:
            print(message)

    def show_alert_popup(self, filename):
        """Displays a UI popup when steganography is detected."""
        if 'Popup' not in globals():
            print(f"ALERT POPUP (Simulated): {filename}")
            return

        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        message = Label(
            text=f"[b][color=ff3333]CRITICAL ALERT[/color][/b]\n\n"
                 f"Hidden information detected in:\n[i]{filename}[/i]\n\n"
                 f"Probability of Steganography: High",
            markup=True,
            halign='center'
        )
        content.add_widget(message)
        close_btn = Button(text="Dismiss", size_hint_y=None, height=40)
        content.add_widget(close_btn)
        popup = Popup(
            title="Security Warning",
            content=content,
            size_hint=(0.8, 0.5),
            auto_dismiss=False
        )
        close_btn.bind(on_release=popup.dismiss)
        popup.open()

if __name__ == '__main__':
    StegoApp().run()
