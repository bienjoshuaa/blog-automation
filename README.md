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



