# Jenquin.io — v1 demo

This is a single-page **Jenquin Dashboard** mock that mirrors your Apple system:
- **Top 3 Today**
- **7-Day Crash Plan**
- **Calendar (next 7 days)**
- Quick Add + “Reveal in Reminders/Calendar” (simulated)

## Run locally (no backend required)
Double-click `index.html` to open in your browser **or** run a local server:

```bash
cd jengquin_site
python3 -m http.server 8080
# open http://localhost:8080
```

## Hooking up a backend later
When your Flask/FastAPI endpoints are ready:
1. Replace `apiGet`/`apiPost` in `script.js` to call real endpoints.
2. Wire buttons (Reveal/Open) to routes that trigger AppleScript on your Mac.

## Deploy via Tailscale (optional)
Expose your local port (e.g., 8080) with **Tailscale Funnel**:

```bash
tailscale funnel 8080
```

Keep ACLs private unless you intend to share publicly.
