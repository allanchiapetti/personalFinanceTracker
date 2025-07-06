// pages/statistics.js
"use client";
import Charts from "@/components/Charts";

export default function StatisticsPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-6">
      <h1 className="text-2xl font-bold mb-4 text-center">Spending Overview</h1>
      <Charts />
    </div>
  );
}