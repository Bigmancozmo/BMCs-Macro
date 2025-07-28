import requests
import ctypes
import webbrowser

REPO = "Bigmancozmo/BMCs-Macro"
CURRENT_VERSION = "1.0.0"
API_URL = f"https://api.github.com/repos/{REPO}/releases/latest"

def check_update():
    r = requests.get(API_URL)
    data = r.json()
    latest_version = data["tag_name"]

    if latest_version != CURRENT_VERSION:
        release_url = data["html_url"]
        response = ctypes.windll.user32.MessageBoxW(
            0,
            f"A new version ({latest_version}) is available.\nOpen GitHub release?",
            "Update Available",
            1
        )
        if response == 1:  # OK clicked
            webbrowser.open(release_url)
