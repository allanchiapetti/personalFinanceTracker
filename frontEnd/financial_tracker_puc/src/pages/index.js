"use client";
import { useSession } from "next-auth/react";
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import Link from "next/link";


export default function IndexPage() {
  
  // Check if the user is already logged in
  const { data: session } = useSession();
  const router = useRouter();
  
  // If session exists, redirect to welcome page
  useEffect(() => {
    if (session) {
      const baseUrl = process.env.NEXT_PUBLIC_BASE_URL;
      router.push(`${baseUrl}/welcome`);
    }
  }, [session, router]);
  return (
    <div className="flex justify-center items-center h-screen">
      <Link href="/auth/login">
        <button className="px-6 py-3 text-lg font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition">
          Login
        </button>
      </Link>
    </div>

  );

}