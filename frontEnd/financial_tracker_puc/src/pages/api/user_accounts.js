import https from 'https';

export default async function handler(req, res) {
  const cookie = req.headers.cookie;

  const agent = new https.Agent({ rejectUnauthorized: false });

  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/accounts`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Cookie: cookie
    },
    agent // Node fetch uses this to accept the self-signed cert
  });

  const data = await response.json();
  console.log(data); // Log the response data for debugging
  res.status(200).json(data);
}