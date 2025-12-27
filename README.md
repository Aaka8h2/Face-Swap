# 🎭 AI Face Swap Pro

> **Premium AI Face Swap App** with built-in Authentication, Credit System, and Local History.  
> **Developed by:** [@aaka8h](https://t.me/aaka8h)

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![Vercel](https://img.shields.io/badge/Deploy-Vercel-black.svg)

## 🌟 Overview

This is a **Serverless Web Application** designed to perform high-quality AI face swaps. It solves the problem of stateless hosting (like Vercel) by using a **Client-Side Database System**, ensuring users can sign up, log in, and maintain credits without a dedicated backend database.

## ✨ Key Features

### 🔐 Secure Authentication
* **No Database Required:** Uses Browser LocalStorage to manage user sessions securely.
* **Privacy First:** User credentials and history are stored on the user's device, not on the server.
* **Multi-User Support:** Supports multiple accounts on the same browser (cleverly separated).

### 💎 Smart Credit System
* **Welcome Bonus:** Every new signup gets **5 Free Credits**.
* **Usage Tracking:** 1 Swap = 1 Credit.
* **Live Updates:** Credits update instantly after every swap.

### 🎨 Modern UI/UX
* **Glassmorphism:** A beautiful, dark-themed UI with frosted glass effects.
* **Responsive:** Works perfectly on Mobile, Tablet, and Desktop.
* **History:** Automatically saves the last 6 generated images locally.

---

## 🚀 How to Run Locally

1.  **Clone this repository:**
    ```bash
    git clone https://github.com/Aaka8h2/Face-Swap.git
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    python app.py
    ```

4.  **Open in Browser:**
    Go to `http://localhost:5000`

---

## ☁️ How to Deploy on Vercel

This app is pre-configured for **Vercel**.

1.  Upload this code to your **GitHub**.
2.  Go to **Vercel Dashboard** > **Add New Project**.
3.  Import your repository.
4.  Vercel will detect `app.py` and `vercel.json` automatically.
5.  Click **Deploy**.

---

## 📞 Contact & Support

For full source code, customization, or API integration support, contact the developer:

* **Telegram:** [@aaka8h](https://t.me/aaka8h)
* **Channel:** [Join Telegram Channel](https://t.me/binarry0)

---

### ⚠️ Disclaimer
This tool is for educational purposes only. The face swap technology is powered by third-party APIs. Please use responsibly.

Copyright © 2025 @aaka8h2. All rights reserved.