# 📸 Photography Invoice Manager

A sleek, minimal web-based invoice management system for photographers. Easily create, manage, and email professional invoices for your clients. Built using Flask, SQLite, and Bootstrap 5.

![Invoice UI Screenshot](screenshot.png) <!-- Optional image preview -->

---

## ✨ Features

- 🧾 Create & edit invoices with line items
- 📧 Send styled invoices via email to clients
- 📅 Store event and due dates
- 🌐 Include album/gallery links
- 📊 Automatic tax and total calculations
- 🔒 SQLite backend with auto-migration
- 🎨 Clean, responsive Bootstrap UI

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yashodsm/Invoice_system_for_photography
cd Invoice_system_for_photography

```
### 2. Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
Install required packages:

```bash

pip install -r requirements.txt

or

pip install flask flask-mail

```
### 3. Configure Email (Flask-Mail)
```bash
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='your_email@gmail.com',
    MAIL_PASSWORD='your_email_app_password',
)

```
💡 For Gmail, generate an App Password from your Google account settings.


### 4. Run the App
```bash
python app.py
```

#### Open your browser:

http://127.0.0.1:5000

### 🧠 Tech Stack
Backend: Flask (Python)

Database: SQLite (auto-created)

Frontend: HTML, Bootstrap 5

Email: Flask-Mail (SMTP)


### 📂 Project Structure

invoice-manager/
├── app.py
├── invoices.db           # Auto-created SQLite database
├── templates/
│   ├── home.html         # Dashboard / Invoice list
│   └── create_edit.html  # Invoice creation form
├── static/               # Optional for CSS/JS/assets
├── README.md
└── requirements.txt      # Python dependencies


### 👨‍💻 Created By
Photography Tools
Built with ❤️ by Yashod


---

### ✅ Next Steps

- Replace:
  - `your_email@gmail.com` with your real email
  - `your_email_app_password` with your app password
  - `yourusername` with your GitHub username
  - `[Your Name]` with your real or company name
- Add `requirements.txt` using:

```bash
pip freeze > requirements.txt
