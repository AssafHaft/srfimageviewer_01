// GitHub API CORS Proxy for Vercel/Netlify
// Deploy this as a serverless function

export default async function handler(req, res) {
  // Only allow POST requests
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { url, method = 'GET', headers = {}, body } = req.body;

  if (!url || !url.startsWith('https://api.github.com/')) {
    return res.status(400).json({ error: 'Invalid URL' });
  }

  try {
    const response = await fetch(url, {
      method: method,
      headers: {
        ...headers,
        'User-Agent': 'GitHub-Image-Manager'
      },
      body: body ? JSON.stringify(body) : undefined
    });

    const data = await response.json();

    // Forward CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

    res.status(response.status).json(data);
  } catch (error) {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.status(500).json({ error: error.message });
  }
}

// Handle OPTIONS for CORS preflight
export async function options(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  res.status(200).end();
}

