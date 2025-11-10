# GitHub API CORS Proxy

This is a serverless function that acts as a CORS proxy for GitHub API calls.

## Deployment Options

### Option 1: Vercel (Recommended)

1. Install Vercel CLI: `npm i -g vercel`
2. In the project root, run: `vercel`
3. Follow the prompts to deploy
4. Update `index.html` to use your Vercel URL as the CORS proxy

### Option 2: Netlify

1. Create a `netlify.toml` file:
```toml
[build]
  functions = "api"
```

2. Deploy to Netlify
3. Update `index.html` to use your Netlify URL

### Option 3: Use Existing CORS Proxy

You can use a public CORS proxy service (not recommended for production):
- Update `USE_CORS_PROXY = true` in `index.html`
- Set `CORS_PROXY = 'https://your-proxy-url.com/'`

## Security Note

This proxy forwards your GitHub token. For production:
- Add authentication to the proxy
- Rate limiting
- Validate requests
- Use environment variables for sensitive config

