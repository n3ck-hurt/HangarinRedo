# Hangarin Arms

Gun store inventory and sales dashboard (Django), with red/black/white theme.

## Setup

```powershell
cd HangarinRedo
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copy environment variables:

```powershell
copy projectsite\.env.example projectsite\.env
```

Edit `projectsite\.env` with your `SECRET_KEY` and optional Google OAuth credentials.

## Run

From the repo root:

```powershell
.\runserver.ps1
```

Or manually:

```powershell
cd projectsite
..\venv\Scripts\python.exe manage.py migrate
..\venv\Scripts\python.exe manage.py setup_site
..\venv\Scripts\python.exe manage.py runserver
```

Open http://127.0.0.1:8000/

## PWA

The app is installable as a Progressive Web App (manifest + service worker). After `collectstatic`, icons and offline support are under `static/pwa/`.

## Deploy (PythonAnywhere + Google OAuth)

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for full steps: WSGI, static files, `.env`, Google Cloud redirect URIs, and PWA on HTTPS.
