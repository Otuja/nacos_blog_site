# 📝 Nacos Blog Site

A simple, modern Django-based blog platform designed for content creation, sharing, and discussion. Built for NACOS students and anyone who wants a clean, minimal blog to share ideas and updates.

## 🚀 Features

- 🧾 Create, edit, and delete blog posts
- 🏷️ Tag posts using `django-taggit`
- 📬 Comment on posts
- 🕵️‍♂️ Admin interface for post management
- 💌 Email notifications (via Gmail SMTP)
- 🔁 Live reload with `django-browser-reload`
- 📁 Image/media uploads
- 🔐 Secure CSRF and host settings
- 🗃️ PostgreSQL-ready for deployment on Render

## 🛠️ Tech Stack

- Python 3.12
- Django 5.2
- SQLite (development) / PostgreSQL (production)
- HTML, CSS (with `widget-tweaks`)
- Taggit for tagging
- Gmail SMTP for email functionality

## 📦 Installation

```bash
git clone https://github.com/Otuja/nacos_blog_site.git
cd nacos_blog_site
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
pip install -r requirements.txt


## 🔐 Environment Variables
Create a .env file in the root directory and add the following:

SECRET_KEY=your_django_secret_key
DEBUG=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
💡 You can generate EMAIL_HOST_PASSWORD as an App Password from your Gmail account settings (if 2FA is enabled).

## 🏃‍♂️ Running the Project

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
Access the site at http://127.0.0.1:8000