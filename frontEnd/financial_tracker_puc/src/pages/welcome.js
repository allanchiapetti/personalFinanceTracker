"use client";
import { useSession, signOut } from "next-auth/react";
import React from "react";
import Link from "next/link";

export default function WelcomePage() {
  // If session does not exist, create a login link
  const { data: session } = useSession();
  
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
  
  document.cookie =  session.user.jwt
  
  return (
    <div>
      <h1>Hello {session.user.first_name}</h1>
      <p>Welcome to the financial tracker app!</p>
      
       
      <div className="flex items-center justify-center h-screen">
          <div className="grid grid-cols-3 gap-6">
              
              <Link href="/expenses/manage">
                <button className="px-6 py-3 bg-blue-500 text-white rounded-lg">Manage transactions</button>
              </Link>

              <Link href="/accounts/manage">
                <button className="px-6 py-3 bg-green-500 text-white rounded-lg">Manage accounts</button>
              </Link>

              <Link href="/expenses/statistics">
                <button className="px-6 py-3 bg-purple-500 text-white rounded-lg">Statistics</button>
              </Link>

          </div>
          
      </div>
      <div>
        <button onClick={() => signOut()}>Sign Out</button>
      </div>
    </div>
  );
};
}