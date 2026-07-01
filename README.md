# 🤖 Jarvis Voice Assistant

A modern desktop-inspired **Jarvis Voice Assistant** built using **Python**, **Flask**, **JavaScript**, **HTML**, **CSS**, and **SQLite**. The application provides voice-controlled desktop automation, user authentication, and a clean web interface.

---

## 📌 Project Overview

Jarvis Voice Assistant is a web-based virtual assistant that performs various system and web operations using voice commands. Users can log in securely, interact with the assistant through the browser, and execute predefined commands such as opening applications, searching the web, controlling system settings, checking the weather, and much more.

---

## ✨ Features

### 🔐 User Authentication

* User Login
* User Registration
* Forgot Password Page
* Admin Dashboard
* User Dashboard
* SQLite Database

### 🎙️ Voice Assistant Features

* Voice Command Recognition
* Greeting Messages
* Current Time & Date
* Weather Information
* Wikipedia Search
* Google Search
* Open YouTube
* Open Google
* Open ChatGPT
* Play YouTube Videos
* Play Music
* Screenshot Capture

### 💻 System Controls

* Open Notepad
* Open Calculator
* Open Paint
* Open Camera
* Open File Explorer
* Open Microsoft Word
* Open Microsoft Excel
* Open PowerShell
* Open Command Prompt
* Open Chrome

### 📂 File & Folder Management

* Open Downloads
* Open Documents
* Open Desktop
* Open Pictures
* Open Videos
* Open Music Folder
* Open Files by Name
* Open Files Using Full Path

### 🔊 Multimedia Controls

* Volume Up
* Volume Down
* Mute / Unmute
* Brightness Control
* Play / Pause Media
* Next Track
* Previous Track

### 🌐 Network Controls

* WiFi On/Off
* Bluetooth On/Off
* Display IP Address

### 📊 System Monitoring

* CPU Usage
* RAM Usage
* Battery Status

---

# 🛠️ Technologies Used

## Frontend

* HTML5
* CSS3
* JavaScript

## Backend

* Python
* Flask

## Database

* SQLite

## Python Libraries

* Flask
* sqlite3
* requests
* wikipedia
* pyautogui
* psutil
* pycaw
* screen-brightness-control
* comtypes
* threading

---

# 📁 Project Structure

```
Jarvis-Voice-Assistant/
│
├── app.py
├── init_db.py
├── jarvis.db
├── requirements.txt
├── README.md
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── forgot_password.html
│   ├── admin_dashboard.html
│   ├── user_dashboard.html
│   ├── jarvis.html
│   └── help.html
│
└── screenshots/
```

---

# ⚙️ Installation


### Navigate to Project

```bash
cd Jarvis-Voice-Assistant
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Virtual Environment

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Create SQLite Database

```bash
python init_db.py
```

### Run Application

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---



# 🚀 Future Enhancements

* Speech-to-Text using SpeechRecognition
* AI Chat Integration
* Face Recognition Login
* Email Assistant
* Task Scheduler
* Calendar Integration
* News Updates
* Voice Authentication
* Smart Home Integration
* Mobile Responsive Dashboard

---

# 👨‍💻 Developer

**Shiva-Tirumani**

**Course:** Master of Computer Applications (MCA) 

**Project:** Jarvis Voice Assistant (Mini Projectgit status)

---

# 📄 License

This project is developed for educational and academic purposes.

---

## ⭐ If you found this project useful, please consider giving it a star on GitHub.
