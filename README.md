# 💒 Wedding Website App

This is a Django-based web application for managing and displaying wedding event information. It allows guests to:

* View details about the wedding day
* Submit RSVPs
* Choose their meal preferences
* Suggest songs for the wedding playlist
* See a live countdown to the event

## 🚀 Features

* Event countdown timer
* RSVP form with guest name, attendance, and meal selection
* Song suggestion form
* Admin panel to view and manage submissions

## 🛠️ Setup Instructions

### Prerequisites

* Python 3.9+
* pip
* [Poetry](https://python-poetry.org/) (or `pip` if preferred)
* PostgreSQL or SQLite (for development)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/wedding-website.git
cd wedding-website
```

### 2. Set Up a Virtual Environment

Using Poetry:

```bash
poetry install
poetry shell
```

Or using venv and pip:

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite:///db.sqlite3  # Or use PostgreSQL URI
```

### 4. Apply Migrations

```bash
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Run the Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to see the site.

---

## 🧪 Development Notes

* Static files are served via Django in development.
* Use the admin site to manage RSVPs, meals, and song suggestions.
* Templates use Django's templating system.

## ✅ TODO / Roadmap

* Email confirmation for RSVPs
* Export RSVPs to CSV
* Guest login with access codes
* Mobile-friendly styling

---

## 📂 Project Structure (Simplified)

```
wedding_website/
├── wedding/             # Main app (views, models, forms)
├── templates/           # HTML templates
├── static/              # CSS/JS/assets
├── manage.py
└── .env.example         # Example env vars
```

---

## 📃 License

MIT License

