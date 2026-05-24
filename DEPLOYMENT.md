# Deploy Hangarin Arms (PythonAnywhere + Google OAuth + PWA)

Replace `yourusername` with your PythonAnywhere account name (e.g. `wrenchnickhurt`).

---

## 1. Push code to PythonAnywhere

1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com).
2. Open a **Bash** console.
3. Clone or upload the project, for example:

```bash
cd ~
git clone https://github.com/YOUR_USER/HangarinRedo.git
# or upload a zip and unzip
```

Project layout on the server should look like:

```
/home/yourusername/HangarinRedo/
  venv/
  requirements.txt
  projectsite/
    manage.py
    .env          ← create this (not in git)
    static/
    templates/
```

---

## 2. Virtual environment and packages

```bash
cd ~/HangarinRedo
python3.10 -m venv venv   # use the Python version shown on your PA Web tab
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

If `mysqlclient` fails to build and you use **SQLite** (default), you can temporarily remove `mysqlclient` from `requirements.txt` on the server, or install system headers per PythonAnywhere’s MySQL docs.

---

## 3. Environment file (`.env`)

```bash
cd ~/HangarinRedo/projectsite
cp .env.example .env
nano .env
```

Example for production:

```env
SECRET_KEY=your-long-random-secret-here
DEBUG=False
ALLOWED_HOSTS=yourusername.pythonanywhere.com
CSRF_TRUSTED_ORIGINS=https://yourusername.pythonanywhere.com

GOOGLE_CLIENT_ID=123456789-xxxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxxxxxxx

SITE_DOMAIN=yourusername.pythonanywhere.com
```

Generate a secret key locally:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 4. Database and static files

```bash
cd ~/HangarinRedo/projectsite
source ../venv/bin/activate

python manage.py migrate
python manage.py setup_site
python manage.py collectstatic --noinput
python manage.py createsuperuser   # optional admin user
```

`setup_site` sets Django **Sites** to `yourusername.pythonanywhere.com` (from `SITE_DOMAIN` or default).

---

## 5. Web app (WSGI)

1. PythonAnywhere → **Web** → **Add a new web app** → Manual configuration → same Python version as your venv.
2. **Virtualenv** (required): `/home/yourusername/HangarinRedo/venv`  
   If this is empty, PythonAnywhere uses system Django and imports often fail.
3. Edit the **WSGI** file: `/var/www/yourusername_pythonanywhere_com_wsgi.py`

**Important:** `sys.path` must point at the folder that contains **`manage.py`** and the inner **`projectsite/`** package (settings), not the repo root `HangarinRedo/`.

```python
import os
import sys

# ← manage.py lives here
PROJECT_ROOT = '/home/yourusername/HangarinRedo/projectsite'

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectsite.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

A ready-made template for account `estaresyodj223` is in the repo: `projectsite/wsgi_pythonanywhere.py`.

4. Verify on a Bash console:

```bash
ls /home/yourusername/HangarinRedo/projectsite/manage.py
ls /home/yourusername/HangarinRedo/projectsite/projectsite/settings.py
source /home/yourusername/HangarinRedo/venv/bin/activate
cd /home/yourusername/HangarinRedo/projectsite
python -c "import projectsite.settings; print('OK')"
```

If that prints `OK`, reload the web app.

### Fix: `ModuleNotFoundError: No module named 'projectsite'`

| Cause | Fix |
|--------|-----|
| Wrong `sys.path` | Use `.../HangarinRedo/projectsite`, not `.../HangarinRedo` |
| Path typo / project not uploaded | Run `ls` and match the real path on the server |
| No virtualenv on Web tab | Set **Virtualenv** to `/home/yourusername/HangarinRedo/venv` and reload |
| `sys.path` added after `get_wsgi_application()` | Add path **before** importing Django |

5. **Static files** mapping (Web tab → Static files):

| URL           | Directory                                              |
|---------------|--------------------------------------------------------|
| `/static/`    | `/home/yourusername/HangarinRedo/projectsite/staticfiles` |

Run `collectstatic` after every deploy that changes CSS/JS/PWA assets.

6. Click **Reload** on the Web tab.

Your site: `https://yourusername.pythonanywhere.com`

---

## 6. Google OAuth (django-allauth)

### A. Google Cloud Console

1. Go to [Google Cloud Console → Credentials](https://console.cloud.google.com/apis/credentials).
2. Create a project (if needed).
3. **APIs & Services → OAuth consent screen**  
   - User type: **External** (or Internal for Workspace).  
   - Fill app name (e.g. **Hangarin Arms**), support email, save.
4. **Credentials → Create credentials → OAuth client ID**  
   - Application type: **Web application**  
   - **Authorized JavaScript origins** (optional for this flow):  
     - `https://yourusername.pythonanywhere.com`
   - **Authorized redirect URIs** (required):
     - `https://yourusername.pythonanywhere.com/accounts/google/login/callback/`
5. Copy **Client ID** and **Client secret** into `projectsite/.env`.

### B. Django on the server

```bash
cd ~/HangarinRedo/projectsite
source ../venv/bin/activate
python manage.py setup_site
```

Confirm output shows:

`Google redirect URI: https://yourusername.pythonanywhere.com/accounts/google/login/callback/`

That URI must match Google Console **exactly** (https, no trailing path typos).

### C. Reload and test

1. Reload the web app on PythonAnywhere.
2. Open `https://yourusername.pythonanywhere.com/accounts/login/`
3. Use **Continue with Google** (shown when `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, and `cryptography` are installed).

### Common OAuth errors

| Problem | Fix |
|--------|-----|
| `redirect_uri_mismatch` | Redirect URI in Google must match callback URL exactly |
| Google button missing | Check `.env` values; run `pip install cryptography`; reload WSGI |
| CSRF / login fails on HTTPS | Set `CSRF_TRUSTED_ORIGINS=https://yourusername.pythonanywhere.com` |
| Wrong callback host | Run `setup_site` with `SITE_DOMAIN=yourusername.pythonanywhere.com` |

---

## 7. PWA (Progressive Web App)

PWA is built in (no extra pip package):

- **Manifest**: `https://yourusername.pythonanywhere.com/manifest.webmanifest`
- **Service worker**: `https://yourusername.pythonanywhere.com/service-worker.js`
- **Offline page**: `/offline/`
- **Icons**: `static/pwa/icon-192.png`, `icon-512.png`

### Requirements for “Install app”

- Site served over **HTTPS** (PythonAnywhere free accounts include HTTPS).
- Valid manifest + registered service worker (included in `base.html` / `base_auth.html`).
- User visits the site in Chrome/Edge (desktop or Android).

### After deploy

1. Run `collectstatic` so `/static/pwa/*` is served.
2. Open the site → DevTools → **Application** → **Manifest** / **Service workers** to verify.
3. On mobile Chrome: menu → **Install app** or **Add to Home screen**.

Logged-in pages still need network; offline mode shows `/offline/` when navigation fails.

### Verify PWA (local or on server)

```bash
cd ~/HangarinRedo/projectsite
source ../venv/bin/activate
python manage.py check_pwa
```

In Chrome: **DevTools → Application → Manifest** and **Service workers** (must be HTTPS on PythonAnywhere).

### Update PWA cache after changes

Edit `CACHE_VERSION` in `projectsite/static/pwa/service-worker.js`, then:

```bash
python manage.py collectstatic --noinput
```

Reload the web app. Users get the new cache on next visit.

---

## 8. Quick checklist

- [ ] Code on PythonAnywhere  
- [ ] `venv` + `pip install -r requirements.txt`  
- [ ] `projectsite/.env` with `SECRET_KEY`, `DEBUG=False`, hosts, Google keys  
- [ ] `migrate`, `setup_site`, `collectstatic`  
- [ ] WSGI points to `projectsite`  
- [ ] Static files URL `/static/` → `staticfiles`  
- [ ] Google redirect URI matches `/accounts/google/login/callback/`  
- [ ] Web app reloaded  
- [ ] PWA manifest + service worker load over HTTPS  

---

## 9. Local vs production

| Setting | Local | PythonAnywhere |
|--------|--------|----------------|
| `DEBUG` | `True` | `False` |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | `yourusername.pythonanywhere.com` |
| Google redirect | `http://127.0.0.1:8000/accounts/google/login/callback/` | `https://yourusername.pythonanywhere.com/accounts/google/login/callback/` |
| PWA install | `localhost` may limit install; use HTTPS tunnel or test on PA | Full PWA on HTTPS |

Local Google OAuth: add `http://127.0.0.1:8000/accounts/google/login/callback/` as a second redirect URI in Google Console and run `SITE_DOMAIN=127.0.0.1:8000 python manage.py setup_site`.
