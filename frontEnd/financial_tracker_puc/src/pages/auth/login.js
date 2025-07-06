"use client";
import { signIn, useSession } from "next-auth/react";
import { useState } from "react";
import { useRouter } from 'next/navigation';    

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const router = useRouter();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const baseUrl = process.env.NEXT_PUBLIC_BASE_URL;
    await signIn("credentials", { email, password, redirect: false });
    // After successful sign-in, redirect to welcome page
    router.push(`${baseUrl}/welcome`);
  };
  
  // Check if the user is already logged in
  const { data: session } = useSession();
  
  // If session exists, redirect to welcome page
  if (session) {

     // Redirect to welcome page
    const baseUrl = process.env.NEXT_PUBLIC_BASE_URL;
    router.push(`${baseUrl}/welcome`);
  }

  return (
    <div>
      <title>Login</title>
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <div className="flex justify-center items-center h-screen bg-gray-100">
        <form onSubmit={handleSubmit} className="bg-white shadow-lg rounded-lg p-8 w-96">
          <input className="w-full p-3 mb-3 border rounded text-gray-900" type="email" placeholder="Email" onChange={(e) => setEmail(e.target.value)} />
          <input className="w-full p-3 mb-3 border rounded text-gray-900" type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} />
          <button  className="w-full p-3 bg-blue-500 text-white rounded" type="submit">Sign In</button>
        </form>
      </div>
    </div>
  );
}