// components/Layout.js
import { useRouter } from "next/router";
import { useSession, signOut } from "next-auth/react";

export default function Layout({ children }) {
  const router = useRouter();
  
  const handleSignOut = async () => {
    //await fetch("/api/signout", { method: "POST" });
    document.cookie = "jwt=123;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/";
    signOut({ redirect: false});
    const baseUrl = process.env.NEXT_PUBLIC_BASE_URL;
    const callback_url = `${baseUrl}/auth/login`;
    router.push(callback_url);
  };

  return (
    <div className="relative min-h-screen">
      <main className="p-4">{children}</main>
    
      <button
        onClick={handleSignOut}
        className="fixed bottom-6 right-6 bg-red-500 text-white px-4 py-2 rounded-full shadow-lg hover:bg-red-600"
      >
        Sign Out
      </button>
    </div>
  );
}