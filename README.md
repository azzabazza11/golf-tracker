# Golf Shot Tracker

Single-file web app for tracking shot distances with GPS on the course.

## Why Chrome shows raw HTML

If you see the source code instead of the app, one of these is usually the cause:

| Cause | Fix |
|-------|-----|
| Opened in an editor or file preview | Use a browser URL, not the IDE preview |
| Wrong app on Android (text viewer) | Open with **Chrome** |
| Downloaded copy named `index.html.txt` | Rename to `index.html` |
| Link served as `text/plain` | Use the dev server below (sets correct MIME types) |
| `file://` path pasted wrong | Use `http://localhost` or `https://` instead |

**Important:** Opening `file:///.../index.html` directly will load the page in many cases, but **GPS will not work**. Browsers require a secure context (`https://` or `http://localhost`).

## Run locally (recommended)

```bash
cd golf-tracker
python3 serve.py
```

Then open **https://localhost:8443/** in Chrome.

For your phone on the same Wi‑Fi, use the `https://192.168.x.x:8443/` URL printed by the script. Accept the certificate warning once (self-signed, local dev only).

### HTTP only (desktop GPS test)

```bash
python3 serve.py --http-only --port 8080
```

Open **http://localhost:8080/** — GPS works on the same machine, but not from your phone over the network.

## Requirements

- Python 3
- `openssl` (for HTTPS cert generation, usually pre-installed on Linux)

## Clear saved data

If you hit storage errors, open DevTools → Console and run:

```javascript
localStorage.removeItem("gst_courses");
localStorage.removeItem("gst_rounds");
location.reload();
```


## Phone-only use (no laptop at the course)

Chrome **blocks GPS** for `file://` links. Opening `index.html` from a file picker will show the app but GPS will not work.

**One-time setup:**

1. Copy `phone-package/GolfTracker/` to your phone (or use `golf-tracker-phone.zip`).
2. Install a local server app (e.g. **Simple HTTP Server** on Play Store).
3. Point it at the GolfTracker folder and start.
4. Open **http://127.0.0.1:8080/** in Chrome and **bookmark** it.

After that you only need your phone at the course.

### Tee positions & club selection

- **Tee Off** saves `teePosition` (lat/lon/accuracy) on each hole in saved rounds for future tee averages.
- **Mark Shot** locks GPS at that moment. Walking while picking a club does **not** change the saved distance or position.
