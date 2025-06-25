import https from 'https';

export default async function handler(req, res) {
  const cookie = req.headers.cookie;
  console.log(cookie)
  console.log(req.body);

  const agent = new https.Agent({ rejectUnauthorized: false });

  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/transactions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Cookie: cookie
    },
    body: JSON.stringify(req.body),
    agent
  });

  const status = await response.status;

  console.log(status)
  res.status(200).json({ success: true });
}