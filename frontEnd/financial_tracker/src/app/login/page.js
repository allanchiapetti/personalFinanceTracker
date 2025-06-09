"use client";
import { signIn } from "next-auth/react";
import { useState } from "react";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    await signIn("credentials", { email, password, redirect: true, callbackUrl: "/test" });
  };

  return (
    <div>
      <title>Login</title>
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <div className="flex justify-center items-center h-screen bg-gray-100">
        <form onSubmit={handleSubmit} className="bg-white shadow-lg rounded-lg p-8 w-96">
          <input className="w-full p-3 mb-3 border rounded" type="email" placeholder="Email" onChange={(e) => setEmail(e.target.value)} />
          <input className="w-full p-3 mb-3 border rounded" type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} />
          <button  className="w-full p-3 bg-blue-500 text-white rounded" type="submit">Sign In</button>
        </form>
      </div>
    </div>
  );
}