## AutoBlog (Django + Cohere) — Beginner Guide

Generate full, styled blog posts from a topic in seconds. This app uses Django (backend) and Cohere Chat API (AI text). It includes responsive HTML/CSS and a clean UI.

### What you can do
- Enter a topic, get a complete blog: title, intro, sections, takeaways, conclusion
- Mobile-friendly layout with readable typography
- Posts saved to a local SQLite database

### Requirements
- Python 3.11 (recommended)
- A Cohere API Key

### 1) Download or clone this project
If you already have the files locally, skip to step 2.

```bash
git clone <your-repo-url>
cd "blog-automation"
```

### 2) Create a virtual environment (Windows PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

If you see an error about the Cohere version, run:
```powershell
.venv\Scripts\python.exe -m pip install --upgrade cohere
```

### 3) Add your environment variables
Create a file named `.env` in the project root (same folder as `manage.py`) with:
```
DJANGO_SECRET_KEY=change-me
DEBUG=True
COHERE_API_KEY=your-real-cohere-key
```

### 4) Set up the database
```powershell
.venv\Scripts\python.exe manage.py migrate
```

### 5) Run the server
```powershell
.venv\Scripts\python.exe manage.py runserver
```
Open `http://127.0.0.1:8000` in your browser.

### 6) Use the app
- Home shows recent posts
- Click “Generate” to create a new post
- Enter a short topic (e.g., "Mindful productivity for students"), submit
- You’ll be redirected to the post detail page

### Troubleshooting
- "ImportError: cannot import name 'config' from 'decouple'" 
  - Make sure you’re using the virtualenv Python: `.venv\Scripts\python.exe manage.py runserver`
  - Or install: `.venv\Scripts\python.exe -m pip install python-decouple`

- Cohere 404 message about Generate API
  - The app uses Cohere Chat API, not Generate. If you see 404s, ensure you’re on a current `cohere` package (e.g., 5.18+):
    ```powershell
    .venv\Scripts\python.exe -m pip install --upgrade cohere
    ```

- "Model removed" errors
  - Models change over time. The app uses `command-a-03-2025`. If that changes, update in `bloggen/views.py` (the `model=` value in the chat call).

- Bold/italics not rendering
  - The app converts simple Markdown (`**bold**`, `*italic*`) to HTML. Regenerate after updating.

- Images not loading or unrelated
  - The app uses Unsplash Source by topic. If you prefer to disable images, we can store empty URLs or use a stable provider with an API key.

### Common commands (Windows)
```powershell
# install packages
.venv\Scripts\python.exe -m pip install -r requirements.txt

# apply migrations
.venv\Scripts\python.exe manage.py migrate

# run server
.venv\Scripts\python.exe manage.py runserver

# create superuser (optional)
.venv\Scripts\python.exe manage.py createsuperuser
```

### Project structure
```
Mental Health/
├─ blog_automation/         # Django project
├─ bloggen/                 # App: models, views, urls
├─ templates/               # HTML templates
├─ static/                  # CSS/JS
├─ db.sqlite3               # Local database (auto-created)
├─ requirements.txt         # Python dependencies
├─ manage.py
└─ .env                     # Your secrets (not committed)
```

### Notes
- Don’t commit `.env` or `db.sqlite3`.
- Always run with the virtual environment Python on Windows: `.venv\Scripts\python.exe ...`

### License
MIT (feel free to use and adapt).

## Blog Automation (Django + Cohere)

### Setup
1. Create `.env` in project root with:
```
DJANGO_SECRET_KEY=change-me
DEBUG=True
COHERE_API_KEY=your-cohere-api-key
```
2. Create virtual env and install deps:
```
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```
3. Migrate and run:
```
.venv\Scripts\python.exe manage.py migrate
.venv\Scripts\python.exe manage.py runserver
```

Open `http://127.0.0.1:8000/` to view. Use `Generate` to create a blog.

### Notes
- API key is loaded from environment via `python-decouple` in `blog_automation/settings.py`.



