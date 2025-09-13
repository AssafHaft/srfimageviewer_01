Put image files in this folder to show them on the TV.

Supported formats: .jpg .jpeg .png .gif .webp .bmp .svg

How images are loaded:
- If a file named manifest.json exists here, the app will load images from it.
  Format options:
    ["image1.jpg", "image2.png"]
    or
    {"images": ["image1.jpg", "image2.png"]}
- Otherwise, the app tries to parse the web server's directory listing for this folder.

Tips:
- If your server does not provide directory listings, create a manifest.json as shown above.
- You can control slide duration and fade in the on-screen controls.
