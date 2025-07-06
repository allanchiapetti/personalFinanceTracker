import https from 'https';

export default async function handler(req, res) {
  const cookie = req.headers.cookie;

  const agent = new https.Agent({ rejectUnauthorized: false });

  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/user`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Cookie: cookie
    },
    body: JSON.stringify(req.body),
    agent
  });

  const status = response.status;

    if (status !== 201) {
        console.error("Error creating user:", errorData);
        return res.status(status).json({ success: false, message: 'User creation failed' });
    } 
    
  res.status(200).json({ success: true });
}