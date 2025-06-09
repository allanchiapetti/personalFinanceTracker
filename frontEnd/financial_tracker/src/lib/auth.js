import axios from "axios";
import { headers } from "next/headers";

export async function authenticateUser(credentials) {
  console.log("Authenticating user with credentials:", credentials);
  try {
    // Set up the request to the API
    const request_json = JSON.stringify({
      email: credentials.email,
      password: credentials.password,
    });

    const request_headers = {'Content-Type': 'application/json'};

    // Make the POST request to the authentication endpoint
    const data = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/auth`, request_json, {headers: request_headers}).then(response => response.data);
    console.log("Authentication successful, received data:", data);
    return data;
  } catch (error) {
    throw new Error("Authentication failed");
  }
}