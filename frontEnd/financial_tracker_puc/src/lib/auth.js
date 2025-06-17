import axios from "axios";
import { headers } from "next/headers";

export async function authenticateUser(credentials) {
  try {
    // Set up the request to the API
    const request_json = JSON.stringify({
      email: credentials.email,
      password: credentials.password,
    });

    const request_headers = {'Content-Type': 'application/json',
                            'Accept': 'application/json',
                            'Access-Control-Allow-Origin': "*",
                            'Access-Control-Allow-Credentials': 'true'};

    // Make the POST request to the authentication endpoint
    const data = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/auth`, request_json, {withCredentials: true, headers: request_headers})//.then(response => response.data);
    console.log("Authentication successful:", data.data);
    console.log("Response headers:", data.headers);
    console.log("Response status:", data.token);
    return {user_id: data.user_id, email: data.email, first_name: data.first_name, last_name: data.last_name,

    }; // Return user details
  } catch (error) {
    throw new Error("Authentication failed");
  }
}