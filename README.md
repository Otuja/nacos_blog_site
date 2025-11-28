# 📝 Nacos Blog Site

A simple, modern Django-based blog platform designed for content creation, sharing, and discussion. Built for NACOS students and anyone who wants a clean, minimal blog to share ideas and updates.

## 🚀 Features

- **Modern UI/UX**: Built with pure Tailwind CSS for a clean, responsive, and professional design.
- **Blog Management**: Create, edit, and delete blog posts with a rich text editor experience.
- **Tagging System**: Organize posts using tags for easy filtering and discovery.
- **Comments**: Engage with readers through a built-in commenting system.
- **Reading Time**: Automatically calculates and displays the estimated reading time for each post.
- **Social Sharing**: Share posts easily via Email, Twitter, Facebook, LinkedIn, and WhatsApp.
- **User Authentication**: Secure login and signup system for authors.
- **Profile Page**: Manage your posts and view your publishing history.
- **Search**: Find articles quickly with a built-in search feature.

## 🛠️ Tech Stack

- **Backend**: Python 3.12, Django 5.2
- **Frontend**: HTML5, Tailwind CSS (Pure), Remix Icons, Google Fonts (Inter)
- **Database**: SQLite (Development) / PostgreSQL (Production ready)
- **Utilities**: 
  - `django-taggit` for tagging
  - `django-widget-tweaks` for form styling
  - `django-browser-reload` for development

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Otuja/nacos_blog_site.git
   cd nacos_blog_site
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv env
   # On Windows
   env\Scripts\activate
   # On macOS/Linux
   source env/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory and add your configuration (see `.env.example` if available, or use standard Django settings).

5. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

8. **Access the application:**
   Open your browser and navigate to `http://127.0.0.1:8000`.

## 📂 Project Structure

- `blog/`: Main application directory.
  - `models.py`: Database models (Post, Comment).
  - `views.py`: View logic for handling requests.
  - `forms.py`: Form definitions.
  - `templates/`: HTML templates.
  - `urls.py`: URL routing.
- `config/`: Project configuration settings.
- `static/`: Static files (CSS, JS, images).
- `media/`: User-uploaded media files.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).