"use client";
import axios from "axios";

export async function getUserPendingTransactions(userId) {
  try {
    // Set up the request to the API
    const request_headers = {'Content-Type': 'text/plain'};

    // Make the GET request to the transactions endpoint
    //const data = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/transactions/pending/${userId}`, {headers: request_headers}).then(response => response.data);
    const data = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/test`, {headers: request_headers, withCredentials: true}).then(response => response.data);

    console.log(data);
    return data; // Return pending transactions
  } catch (error) {
    //throw new Error("Failed to fetch pending transactions");
    console.error("Error fetching pending transactions:", error);}
};