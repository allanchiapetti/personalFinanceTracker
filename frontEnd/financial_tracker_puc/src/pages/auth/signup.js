"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function SignUpPage() {
  const router = useRouter();
  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    // Call your backend /api/signup route (or NextAuth credentials provider)
    const res = await fetch("/api/create_user", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });

    if (res.ok) {
      router.push("/auth/login"); // Go to login after successful signup
    } else {
      alert("Something went wrong. Try again.");
    }
  };

  return (
    <div className="flex justify-center items-center h-screen px-4 bg-gray-50">
      <form
        onSubmit={handleSubmit}
        className="bg-white p-6 rounded-lg shadow-md w-full max-w-md space-y-4"
      >
        <h2 className="text-2xl font-bold text-center text-gray-600">Create an Account</h2>

        <input
          type="text"
          name="first_name"
          value={form.first_name}
          onChange={handleChange}
          required
          placeholder="First Name"
          className="w-full px-4 py-2 border rounded focus:outline-none focus:ring focus:ring-blue-400 transition text-gray-900"
        />

          <input
          type="text"
          name="last_name"
          value={form.last_name}
          onChange={handleChange}
          required
          placeholder="Last Name"
          className="w-full px-4 py-2 border rounded focus:outline-none focus:ring focus:ring-blue-400 transition text-gray-900"
        />


        <input
          type="email"
          name="email"
          value={form.email}
          onChange={handleChange}
          required
          placeholder="Email"
          className="w-full px-4 py-2 border rounded focus:outline-none focus:ring focus:ring-blue-400 transition text-gray-900"
        />

        <input
          type="password"
          name="password"
          value={form.password}
          onChange={handleChange}
          required
          minLength={6}
          placeholder="Password"
          className="w-full px-4 py-2 border rounded focus:outline-none focus:ring focus:ring-blue-400 transition text-gray-900"
        />

        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
        >
          Sign Up
        </button>

        <p className="text-sm text-center text-gray-600">
          Already have an account?{" "}
          <span
            onClick={() => router.push("/auth/login")}
            className="text-blue-600 hover:underline cursor-pointer"
          >
            Login here
          </span>
        </p>
      </form>
    </div>
  );
}