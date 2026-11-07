import os
import sys

# MUST be set before QApplication is initialized
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--autoplay-policy=no-user-gesture-required"
os.environ["QT_QPA_PLATFORM"] = "wayland"

from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineScript, QWebEngineProfile, QWebEnginePage



# Define your TV channels mapping number keys to web URLs / video links
# You can replace these URLs with your actual channel links (e.g., YouTube embeds, HTML5 streams)
CHANNELS = {
    Qt.Key.Key_1: "https://vtvgo.vn/channel/1",
    Qt.Key.Key_2: "https://vtvgo.vn/channel/2",
    Qt.Key.Key_3: "https://vtvgo.vn/channel/3",
}

class PiTVSwitcher(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Window configuration for Raspberry Pi (Full screen / Kiosk mode)
        self.setWindowTitle("Pi TV Channel Switcher")
        self.showFullScreen()

        # 1. Setup a persistent profile so cookies and login sessions are saved to disk
        storage_path = os.path.join(os.getcwd(), "pi_tv_profile")
        self.profile = QWebEngineProfile("PiTVPersistentProfile", self)
        self.profile.setPersistentStoragePath(storage_path)
        self.profile.setCachePath(os.path.join(storage_path, "cache"))
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)
        
        # Bind the custom profile to the web page and view
        self.page = QWebEnginePage(self.profile, self)
        self.browser = QWebEngineView()
        self.browser.setPage(self.page)
        self.setCentralWidget(self.browser)
        
        # Set default startup channel (Channel 1)
        self.current_channel = Qt.Key.Key_1
        if self.current_channel in CHANNELS:
            self.load_channel(self.current_channel)

    def load_channel(self, key):
        url = CHANNELS[key]
        print(f"Switching channel... Loading URL: {url}")
        self.browser.setUrl(QUrl(url))

    def keyPressEvent(self, event):
        key = event.key()
        
        # Check if the pressed key corresponds to a defined channel
        if key in CHANNELS:
            self.current_channel = key
            self.load_channel(key)
        elif key == Qt.Key.Key_Escape:
            # Press ESC to exit the application if needed during development
            self.close()
        else:
            # Pass other keys up to the browser/system
            super().keyPressEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Optional: Enable hardware acceleration flags if video stuttering occurs on older Pi models
    # app.setAttribute(Qt.ApplicationAttribute.AA_UseOpenGLES)
    
    player = PiTVSwitcher()
    player.show()
    sys.exit(app.exec())

