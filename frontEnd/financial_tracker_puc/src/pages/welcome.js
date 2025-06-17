"use client";
import { useSession, signOut } from "next-auth/react";
import React from "react";
import Link from "next/link";

export default function WelcomePage() {
  const { data: session } = useSession();
  document.cookie =  session.user.jwt


  // If session does not exist, create a login link
  if (!session) {
    return    (
      <div className="flex justify-center items-center h-screen">
      <Link href="/auth/login">
        <button className="px-6 py-3 text-lg font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition">
          Login
        </button>
      </Link>
    </div>
  );
}
  else {
  return (
    <div>
      <h1>Hello {session.user.first_name}</h1>
      <p>Welcome to the financial tracker app!</p>
      
       
      <div className="flex items-center justify-center h-screen">
          <div className="grid grid-cols-2 gap-6">
              
              <Link href="/expenses/manage">
                <button className="px-6 py-3 bg-blue-500 text-white rounded-lg">Manage expenses</button>
              </Link>

              <button className="px-6 py-3 bg-green-500 text-white rounded-lg">Button 2</button>

          </div>
          
      </div>
      <div>
        <button onClick={() => signOut()}>Sign Out</button>
      </div>
    </div>
  );
};
}