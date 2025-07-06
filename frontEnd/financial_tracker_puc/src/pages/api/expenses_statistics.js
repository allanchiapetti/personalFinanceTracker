import https from 'https';

export default async function handler(req, res) {
  const cookie = req.headers.cookie;

  const agent = new https.Agent({ rejectUnauthorized: false });

  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/accounts/debit_stats`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Cookie: cookie
    },
    agent // Node fetch uses this to accept the self-signed cert
  });  
  const data = await response.json();

  console.log("Data fetched from API:", data);
  res.status(200).json(data);
}