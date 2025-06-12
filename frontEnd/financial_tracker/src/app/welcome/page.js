"use client";
import { useSession } from "next-auth/react";

export default function Profile() {
  const { data: session } = useSession();

  if (!session) return <p>Not authenticated</p>;

  return (
    <div>
      <h1>Welcome, {session.user.name}!</h1>
      <p>User ID: {session.user.id}</p>
    </div>
  );
}