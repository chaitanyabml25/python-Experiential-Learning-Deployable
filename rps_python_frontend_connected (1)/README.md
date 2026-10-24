# Rock Paper Scissors — Python + Frontend

This project keeps the game calculations in Python and uses HTML/CSS/JavaScript for the interface.

## Project files

- `app.py` — Python Flask backend; handles random computer moves, rules, 25-round limit, scores, streaks, history and reports.
- `frontend/index.html` — user interface and dashboard.
- `frontend/config.js` — backend API URL setting.
- `requirements.txt` — Python packages.
- `render.yaml` — Render deployment configuration.

## 1. Run locally

Install Python 3.10+.

```bash
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

Mac/Linux:
```bash
source venv/bin/activate
```

Install packages and start the server:

```bash
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000` in your browser. The Flask server also serves the frontend locally, so the frontend and backend are already connected.

## 2. Deploy the Python backend to Render

1. Push this whole project to a GitHub repository.
2. Sign in to Render and create **New → Web Service**.
3. Connect the repository.
4. Set **Root Directory** to the project root (leave blank if the files are in the repository root).
5. Set **Build Command** to `pip install -r requirements.txt`.
6. Set **Start Command** to `gunicorn app:app`.
7. Deploy. Copy the service URL, for example `https://your-service.onrender.com`.

The included `render.yaml` can also be used as a Render Blueprint.

## 3. Connect GitHub Pages frontend to Render backend

1. Open `frontend/config.js`.
2. Replace `PASTE_YOUR_RENDER_BACKEND_URL_HERE` with your actual Render URL, without a trailing slash.
   Example:
   ```js
   window.API_BASE_URL = "https://your-service.onrender.com";
   ```
3. Commit and push this change.
4. In GitHub, open **Settings → Pages**.
5. Set **Deploy from a branch**, select `main`, and choose `/ (root)` only if the frontend files are at repository root.

### GitHub Pages setup

The ZIP includes `index.html` and `config.js` at the repository root for GitHub Pages, plus copies inside `frontend/` for local Flask serving.

1. Keep the root-level `index.html` and `config.js` in the repository.
2. Keep `app.py`, `requirements.txt`, `render.yaml`, and the `frontend/` folder too.
3. In GitHub Pages, choose **Deploy from a branch**, branch `main`, folder `/ (root)`.
4. GitHub Pages will publish the root-level frontend files.

## Notes

- GitHub Pages cannot run Python. The Python backend must run on a Python hosting service such as Render.
- The backend currently stores active game sessions in memory. Restarting/redeploying the backend clears active games; this version does not use a database.
- CORS is enabled for straightforward deployment. For a public production project, restrict CORS to your actual GitHub Pages domain.
