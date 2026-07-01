from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# ---------------- DATABASE CONNECTION ----------------

def get_db_connection():
    conn = sqlite3.connect("jarvis.db")
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- HOME ----------------

@app.route("/")
def login():
    return render_template("login.html")


@app.route("/jarvis")
def jarvis():
    return render_template("jarvis.html")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=?",
        (email,)
    )

    user = cursor.fetchone()

    conn.close()

    if user:
        if user["password"] == password:
            if user["role"] == "admin":
                return redirect(url_for("admin_dashboard"))
            else:
                return redirect(url_for("user_dashboard"))

    flash("Invalid Email or Password")
    return redirect(url_for("login"))


# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return render_template("register.html")

    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    password_re = request.form["password_re"]

    if password != password_re:
        flash("Passwords do not match")
        return redirect(url_for("register"))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check existing email
    cursor.execute(
        "SELECT * FROM users WHERE email=?",
        (email,)
    )

    existing = cursor.fetchone()

    if existing:
        flash("Email already exists")
        conn.close()
        return redirect(url_for("register"))

    # Insert new user
    cursor.execute(
        """
        INSERT INTO users(name,email,password,role)
        VALUES(?,?,?,?)
        """,
        (name, email, password, "user")
    )

    conn.commit()
    conn.close()

    flash("Registration Successful! Please Login.")
    return redirect(url_for("login"))


# ---------------- USER ----------------

@app.route("/user-dashboard")
def user_dashboard():
    return render_template("user_dashboard.html")


# ---------------- ADMIN ----------------

@app.route("/admin-dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html")


# ---------------- HELP ----------------

@app.route("/help")
def help_page():
    return render_template("help.html")


# ---------------- FORGOT PASSWORD ----------------

@app.route("/forgot-password")
def forgot_password():
    return render_template("forgot_password.html")





import webbrowser
import os
import subprocess
import datetime
import wikipedia
import requests
import pyautogui
import threading
import platform
from flask import request, jsonify

COMMAND_TOKEN = "local-only-token"


# ------------------------- GREETING -------------------------
def greeting_message():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        return "Good morning sir, welcome back."
    elif hour < 18:
        return "Good afternoon sir, welcome back."
    else:
        return "Good evening sir, welcome back."


# -------------------- WEATHER --------------------
def get_weather(city):
    try:
        url = f"https://wttr.in/{city}?format=%C+%t"
        return requests.get(url, timeout=2).text
    except:
        return "Unable to get weather."


# -------------------- THREAD RUNNER --------------------
def run_async(func, *args):
    thread = threading.Thread(target=func, args=args)
    thread.start()


# -------------------- OPEN WEBSITE --------------------
def open_website(url):
    try:
        webbrowser.open(url)
    except Exception as e:
        print("Error opening website:", e)


# -------------------- OPEN APPLICATION --------------------
def open_app(path):
    try:
        if isinstance(path, list):
            path = path[0]
        subprocess.Popen(path, shell=True)
    except Exception as e:
        print("Error opening app:", e)


# -------------------- VOLUME & BRIGHTNESS --------------------
try:
    from ctypes import POINTER, cast
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    PYCAV_AVAILABLE = True
except:
    PYCAV_AVAILABLE = False

try:
    import screen_brightness_control as sbc
    SBC_AVAILABLE = True
except:
    SBC_AVAILABLE = False


def set_volume_percent(val):
    try:
        if PYCAV_AVAILABLE and platform.system() == "Windows":
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevelScalar(val / 100, None)
            return f"Volume set to {val}%"
        else:
            subprocess.run(["nircmd.exe", "setsysvolume",
                            str(int(65535 * (val / 100)))])
            return f"Volume set to {val}% (fallback)"
    except Exception as e:
        return f"Error setting volume: {e}"


def change_volume(delta):
    try:
        if PYCAV_AVAILABLE and platform.system() == "Windows":
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            current = volume.GetMasterVolumeLevelScalar()
            newp = min(1.0, max(0.0, current + delta / 100))
            volume.SetMasterVolumeLevelScalar(newp, None)
            return f"Volume now {int(newp * 100)}%"
    except:
        pass

    return set_volume_percent(max(0, min(100, delta)))


def toggle_mute():
    try:
        if PYCAV_AVAILABLE:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            m = volume.GetMute()
            volume.SetMute(not m, None)
            return "Muted" if not m else "Unmuted"
    except:
        pass

    subprocess.run(["nircmd.exe", "mutesysvolume", "2"])
    return "Mute toggled."


def set_brightness(val):
    try:
        if SBC_AVAILABLE:
            sbc.set_brightness(val)
            return f"Brightness set to {val}%"

        ps = f'(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{val})'
        subprocess.run(["powershell", "-Command", ps])
        return f"Brightness set to {val}% (fallback)"
    except Exception as e:
        return f"Error setting brightness: {e}"
    

    #newwww--------------
import psutil

# ------------ SYSTEM INFO ------------
def get_system_stats():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    battery = psutil.sensors_battery().percent if psutil.sensors_battery() else "N/A"
    return f"CPU: {cpu}% | RAM: {ram}% | Battery: {battery}%"


# ------------ OPEN COMMON WINDOWS APPS ------------
WINDOWS_APPS = {
    "camera": "microsoft.windows.camera:",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
    "powershell": "powershell.exe",
    "cmd": "cmd.exe",
    "file explorer": "explorer.exe",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe"
}

# -------------------- FILE & FOLDER OPERATIONS --------------------

def open_folder(path):
    try:
        os.startfile(path)
    except Exception as e:
        print("Error opening folder:", e)

def open_any_file(file_path):
    try:
        os.startfile(file_path)
    except Exception as e:
        print("Error opening file:", e)

# Common folders
USER = os.path.expanduser("~")
FOLDERS = {
    "downloads": os.path.join(USER, "Downloads"),
    "documents": os.path.join(USER, "Documents"),
    "desktop": os.path.join(USER, "Desktop"),
    "pictures": os.path.join(USER, "Pictures"),
    "videos": os.path.join(USER, "Videos"),
    "music": os.path.join(USER, "Music"),
}

# -------------------- WIFI & BLUETOOTH --------------------

def wifi_control(state: str):
    """
    state = 'on' or 'off'
    Uses Windows netsh command.
    """
    try:
        cmd = f"netsh interface set interface name=\"Wi-Fi\" admin={state}"
        subprocess.run(cmd, shell=True)
        return f"WiFi turned {state}"
    except Exception as e:
        return f"Error controlling WiFi: {e}"


def bluetooth_control(state: str):
    """
    state = 'on' or 'off'
    Uses Windows PowerShell commands.
    """
    try:
        if state == "on":
            ps = "Get-PnpDevice -Class Bluetooth | Enable-PnpDevice -Confirm:$false"
        else:
            ps = "Get-PnpDevice -Class Bluetooth | Disable-PnpDevice -Confirm:$false"

        subprocess.run(["powershell", "-Command", ps], shell=True)
        return f"Bluetooth turned {state}"
    except Exception as e:
        return f"Error controlling Bluetooth: {e}"







     #----------------------------voice command------
 
@app.route('/voice-command', methods=['POST'])
def voice_command():
    data = request.get_json() or {}
    token = data.get("token", "")
    cmd = (data.get("command") or "").lower().strip()

    if token != COMMAND_TOKEN:
        return jsonify({"reply": "Unauthorized access."}), 401

    # Wake / greeting
    if any(w in cmd for w in ("jarvis", "wake up", "start", "hey jarvis")):
        return jsonify({"reply": greeting_message()})

    # Time & Date
    if "time" in cmd:
        return jsonify({"reply": datetime.datetime.now().strftime("The time is %I:%M %p")})

    if "date" in cmd:
        return jsonify({"reply": datetime.datetime.now().strftime("Today is %d %B %Y")})

    # Weather
    if "weather in" in cmd:
        city = cmd.replace("weather in", "").strip()
        return jsonify({"reply": get_weather(city)})

    # Wikipedia
    if "wikipedia" in cmd:
        try:
            topic = cmd.replace("wikipedia", "").strip()
            summary = wikipedia.summary(topic, sentences=2)
            return jsonify({"reply": summary})
        except:
            return jsonify({"reply": "No Wikipedia results found."})

    # Play on YouTube
    if "play" in cmd and "on youtube" in cmd:
        song = cmd.replace("play", "").replace("on youtube", "").strip()
        url = f"https://www.youtube.com/results?search_query={song}"
        run_async(open_website, url)
        return jsonify({"reply": f"Playing {song} on YouTube."})

    # Website opens
    if "open youtube" in cmd:
        run_async(open_website, "https://youtube.com")
        return jsonify({"reply": "Opening YouTube"})

    if "open google" in cmd:
        run_async(open_website, "https://google.com")
        return jsonify({"reply": "Opening Google"})

    if "open chatgpt" in cmd:
        run_async(open_website, "https://chatgpt.com")
        return jsonify({"reply": "Opening ChatGPT"})

    # Search
    if cmd.startswith("search"):
        q = cmd.replace("search", "").strip()
        url = f"https://www.google.com/search?q={q}"
        run_async(open_website, url)
        return jsonify({"reply": f"Searching for {q}..."})

    # Music
    if "play music" in cmd:
        music_dir = os.path.expanduser("~/Music")
        try:
            songs = os.listdir(music_dir)
            if songs:
                run_async(os.startfile, os.path.join(music_dir, songs[0]))
                return jsonify({"reply": "Playing music."})
        except:
            pass
        return jsonify({"reply": "No music found."})

    # Apps
    if "open notepad" in cmd:
        run_async(open_app, "notepad.exe")
        return jsonify({"reply": "Opening Notepad."})

    # Screenshot
    if "screenshot" in cmd:
        path = os.path.expanduser("~/Pictures/jarvis_screenshot.png")
        run_async(pyautogui.screenshot, path)
        return jsonify({"reply": "Screenshot saved."})

    # Shutdown / restart
    if "shutdown" in cmd:
        run_async(os.system, "shutdown /s /t 1")
        return jsonify({"reply": "Shutting down."})

    if "restart" in cmd:
        run_async(os.system, "shutdown /r /t 1")
        return jsonify({"reply": "Restarting."})
    
    #-----------1. System Stats----------

    if "system status" in cmd or "system info" in cmd:
        return jsonify({"reply": get_system_stats()})


     #-----------Open Windows Apps------

    if "open" in cmd:
        for app in WINDOWS_APPS:
            if app in cmd:
                run_async(open_app, WINDOWS_APPS[app])
                return jsonify({"reply": f"Opening {app}."})
            
#-------------Volume Up / Down---------
   
    if "volume up" in cmd:
        return jsonify({"reply": change_volume(10)})

    if "volume down" in cmd:
        return jsonify({"reply": change_volume(-10)})

    if "mute" in cmd:
        return jsonify({"reply": toggle_mute()})
    
    #--------------Brightness Up / Down-------

    if "brightness up" in cmd:
        return jsonify({"reply": set_brightness( min(100, sbc.get_brightness()[0] + 10) )})

    if "brightness down" in cmd:
        return jsonify({"reply": set_brightness( max(0, sbc.get_brightness()[0] - 10) )})
    
#-----Open Folders (Downloads, Documents, Desktop-----

    if "open downloads" in cmd:
        run_async(os.startfile, os.path.expanduser("~/Downloads"))
        return jsonify({"reply": "Opening Downloads folder."})

    if "open documents" in cmd:
        run_async(os.startfile, os.path.expanduser("~/Documents"))
        return jsonify({"reply": "Opening Documents folder."})

    if "open desktop" in cmd:
        run_async(os.startfile, os.path.expanduser("~/Desktop"))
        return jsonify({"reply": "Opening Desktop folder."})

#-------Lock / Sign out---------

    if "lock system" in cmd or "lock computer" in cmd:
        run_async(os.system, "rundll32.exe user32.dll,LockWorkStation")
        return jsonify({"reply": "System locked."})

    if "sign out" in cmd:
        run_async(os.system, "shutdown /l")
        return jsonify({"reply": "Signing out."})
    
    #-----Media Controls (Play/Pause/Next/Previous)(Works on YouTube, Spotify, VLC, all)--
     
    if "pause" in cmd:
        pyautogui.press("space")
        return jsonify({"reply": "Paused."})

    if "play" in cmd:
        pyautogui.press("space")
        return jsonify({"reply": "Playing."})

    if "next" in cmd:
        pyautogui.hotkey("shift", "n")
        return jsonify({"reply": "Next track."})

    if "previous" in cmd:
        pyautogui.hotkey("shift", "p")
        return jsonify({"reply": "Previous track."})
    
    ###--------------IP Address---------

    if "ip address" in cmd:
        ip = requests.get("https://api.ipify.org").text
        return jsonify({"reply": f"Your IP address is {ip}"})

#----------file exploerr--------------
    if "open file explorer" in cmd or "open explorer" in cmd:
        run_async(os.startfile, "explorer.exe")
        return jsonify({"reply": "Opening File Explorer."})
    
    #------Open Common Folders------------

    for folder_name, folder_path in FOLDERS.items():
        if f"open {folder_name}" in cmd:
            run_async(open_folder, folder_path)
            return jsonify({"reply": f"Opening {folder_name} folder."})

#------Open Any File by Name (Inside Downloads, Desktop, Documents)------

    if "open file" in cmd:
        file_name = cmd.replace("open file", "").strip()

        # search in predefined folders
        for folder_path in FOLDERS.values():
            try:
                for f in os.listdir(folder_path):
                    if file_name.lower() in f.lower():
                        full_path = os.path.join(folder_path, f)
                        run_async(open_any_file, full_path)
                        return jsonify({"reply": f"Opening {f}."})
            except:
                pass

        return jsonify({"reply": f"File '{file_name}' not found in common folders."})
    
#----------------Open File With Full Path------------

    if cmd.startswith("open ") and (":" in cmd or "\\" in cmd):
        file_path = cmd.replace("open", "").strip()
        if os.path.exists(file_path):
            run_async(open_any_file, file_path)
            return jsonify({"reply": f"Opening {file_path}."})
        return jsonify({"reply": "Invalid file path."})
    
    #Open Specific File Inside Folder-----------

    for folder_name, folder_path in FOLDERS.items():
        if f"open {folder_name}" in cmd and folder_name in cmd:
            # extract filename
            file = cmd.replace(f"open {folder_name}", "").strip()

            if file == "":
                run_async(open_folder, folder_path)
                return jsonify({"reply": f"Opening {folder_name} folder."})

            # search inside folder
            try:
                for f in os.listdir(folder_path):
                    if file.lower() in f.lower():
                        run_async(open_any_file, os.path.join(folder_path, f))
                        return jsonify({"reply": f"Opening {f} from {folder_name}."})
                return jsonify({"reply": f"File '{file}' not found in {folder_name} folder."})
            except:
                return jsonify({"reply": "Unable to open folder."})


    # ---------------- WIFI CONTROL ----------------
    if "wifi off" in cmd or "turn off wifi" in cmd or "disable wifi" in cmd:
        return jsonify({"reply": wifi_control("disabled")})

    if "wifi on" in cmd or "turn on wifi" in cmd or "enable wifi" in cmd:
        return jsonify({"reply": wifi_control("enabled")})


    # ---------------- BLUETOOTH CONTROL ----------------
    if "bluetooth off" in cmd or "turn off bluetooth" in cmd or "disable bluetooth" in cmd:
        return jsonify({"reply": bluetooth_control("off")})

    if "bluetooth on" in cmd or "turn on bluetooth" in cmd or "enable bluetooth" in cmd:
        return jsonify({"reply": bluetooth_control("on")})



# Default fallback

    return jsonify({"reply": f"Sorry, I didn't understand: {cmd}"})
if __name__ == "__main__":
    app.run(debug=True)

 