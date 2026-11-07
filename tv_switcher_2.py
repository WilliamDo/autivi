import os
import sys

# MUST be set before QApplication is initialized
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--autoplay-policy=no-user-gesture-required"

from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineScript, QWebEngineProfile, QWebEnginePage

# Define your TV channels mapping number keys to web URLs / video links
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
        self.setWindowFlags(Qt.WindowType.Window)

        # 1. Setup a robust, absolute path for persistent storage in the user's home directory
        storage_path = os.path.expanduser("~/.local/share/pi_tv_profile")
        os.makedirs(storage_path, exist_ok=True) # Ensure directory exists

        self.profile = QWebEngineProfile("PiTVPersistentProfile", self)
        self.profile.setPersistentStoragePath(storage_path)
        self.profile.setCachePath(os.path.join(storage_path, "cache"))
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)

        # Explicitly enforce disk caching so cookies and web session data are written to storage
        self.profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.DiskHttpCache)

        # 2. Inject the CSS crop & autoplay automation script into the profile
        self._inject_automation_script()

        # 3. Create a central widget and zero-margin layout to strip default padding
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Bind the custom profile to the web page and view
        self.page = QWebEnginePage(self.profile, self)
        self.browser = QWebEngineView()
        self.browser.setPage(self.page)

        layout.addWidget(self.browser)

        # Set default startup channel (Channel 1)
        self.current_channel = Qt.Key.Key_1
        if self.current_channel in CHANNELS:
            self.load_channel(self.current_channel)

    def _inject_automation_script(self):
        script = QWebEngineScript()
        script.setName("PiTVCropAndMaximizeScript")

        # JavaScript payload that injects CSS to crop out clutter and force video full screen
        js_code = """
        (function() {
            function applyCropAndMaximize() {
                // 1. Inject custom CSS stylesheet if it doesn't exist yet
                let style = document.getElementById('pi-tv-crop-style');
                if (!style) {
                    style = document.createElement('style');
                    style.id = 'pi-tv-crop-style';
                    style.innerHTML = `
                        /* Hide scrollbars, headers, sidebars, footers, and site clutter */
                        html, body {
                            margin: 0 !important;
                            padding: 0 !important;
                            overflow: hidden !important;
                            background: black !important;
                        }
                        header, footer, nav, .sidebar, .ads, .menu, .header-container {
                            display: none !important;
                        }

                        /* Force the video player container to fill the screen (crops everything else out) */
                        video, .jw-player, .video-js, .player-container {
                            position: fixed !important;
                            top: 0 !important;
                            left: 0 !important;
                            width: 100vw !important;
                            height: 100vh !important;
                            object-fit: contain !important;
                            z-index: 999999 !important;
                        }
                    `;
                    document.head.appendChild(style);
                }

                // 2. Ensure underlying media elements are unmuted and playing
                document.querySelectorAll('video, audio').forEach(function(media) {
                    media.muted = false;
                    media.volume = 1.0;
                    media.play().catch(function(e) {});
                });
            }

            setInterval(applyCropAndMaximize, 1000);
            window.addEventListener('DOMContentLoaded', applyCropAndMaximize);
        })();
        """

        script.setSourceCode(js_code)
        script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentCreation)
        script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
        self.profile.scripts().insert(script)

    def showEvent(self, event):
        super().showEvent(event)
        screen = QApplication.primaryScreen()
        if screen:
            self.setGeometry(screen.geometry())
        self.showFullScreen()

    def load_channel(self, key):
        url = CHANNELS[key]
        print(f"Switching channel... Loading URL: {url}")
        self.browser.setUrl(QUrl(url))

    def keyPressEvent(self, event):
        key = event.key()

        if key in CHANNELS:
            self.current_channel = key
            self.load_channel(key)
        elif key == Qt.Key.Key_0:
            print("Simulating crash / exit via Key 0...")
            sys.exit(0)  # Forces the process to quit so systemd can trigger a restart
        elif key == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    player = PiTVSwitcher()
    player.show()
    sys.exit(app.exec())
