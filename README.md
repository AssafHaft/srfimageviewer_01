# srfimageviewer_01

Reception TV image viewer. Drop images into `images/` and open `index.html` in a browser. If multiple images are present, it loops with a crossfade; a single image stays up indefinitely.

## Dev Manifest Generator

The page prefers an `images/manifest.json` to list images. During development, generate it automatically with the tiny helper below (no dependencies):

- One-off generate:
  - `python scripts/generate_manifest.py`
- Watch and auto-regenerate on changes (add/remove/modify files):
  - `python scripts/generate_manifest.py --watch`
- Options:
  - `--dir PATH` images directory (default: `images/`)
  - `--out PATH` output path (default: `images/manifest.json`)
  - `--interval SEC` polling interval when watching (default: 2.0)

Manifest format written:

```
{
  "generatedAt": "2025-09-13T21:00:00Z",
  "count": 3,
  "images": ["welcome.jpg", "promo.png", "sub/offer.webp"]
}
```

The viewer also works without a manifest if your web server exposes a directory listing for `images/` (e.g., Python’s `http.server`).

## Local Server

- Start a simple server from the repo root:
  - `python -m http.server 8000`
- Visit on the TV browser:
  - `http://<your-computer-ip>:8000/`

## Supported Formats

`.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`, `.bmp`, `.svg`
