"use client";
import { useSession, signIn, signOut } from "next-auth/react";

export default function Profile() {
  const { data: session } = useSession();

  if (!session) {
    return <button onClick={() => signIn()}>Sign In</button>;
  }

  return (
    <div>
      <h1>Test, {session.user.name}!</h1>
      <h2>Test, {session.user.id}!</h2>
      <button onClick={() => signOut()}>Sign Out</button>
    </div>
  );
}