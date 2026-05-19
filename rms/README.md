# Restaurant Management System

A full-stack Django web app built following the MTV (Model-Template-View) pattern.

## Quick Start

```bash
# 1. Create & activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Apply migrations
python manage.py migrate

# 4. (Optional) Create an admin superuser
python manage.py createsuperuser

# 5. Run the development server
python manage.py runserver
```

Visit http://127.0.0.1:8000 — the app is live!
Admin panel: http://127.0.0.1:8000/admin

## URL Reference

| URL         | View               | Description              |
|-------------|--------------------|--------------------------|
| `/`         | restaurant_list    | List all restaurants     |
| `/<pk>/`    | restaurant_detail  | View a single restaurant |
| `/new/`     | restaurant_create  | Add a new restaurant     |
| `/admin/`   | Django Admin       | Admin panel              |
