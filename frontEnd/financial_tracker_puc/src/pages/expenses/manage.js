import React from 'react';
import { getUserPendingTransactions } from '@/lib/transactions';

const TablePage = () => {
    const user_transactions = getUserPendingTransactions(1); // Replace with actual user ID
  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      <div className="w-3/4 bg-white shadow-lg rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4">Data Table</h2>
        <table className="w-full border-collapse border border-gray-300">
          <thead>
            <tr className="bg-gray-200">
              <th className="border border-gray-300 px-4 py-2">ID</th>
              <th className="border border-gray-300 px-4 py-2">Name</th>
              <th className="border border-gray-300 px-4 py-2">Age</th>
              <th className="border border-gray-300 px-4 py-2">Email</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td className="border border-gray-300 px-4 py-2">1</td>
              <td className="border border-gray-300 px-4 py-2">Alice</td>
              <td className="border border-gray-300 px-4 py-2">25</td>
              <td className="border border-gray-300 px-4 py-2">alice@example.com</td>
            </tr>
            <tr className="bg-gray-100">
              <td className="border border-gray-300 px-4 py-2">2</td>
              <td className="border border-gray-300 px-4 py-2">Bob</td>
              <td className="border border-gray-300 px-4 py-2">30</td>
              <td className="border border-gray-300 px-4 py-2">bob@example.com</td>
            </tr>
            <tr>
              <td className="border border-gray-300 px-4 py-2">3</td>
              <td className="border border-gray-300 px-4 py-2">Charlie</td>
              <td className="border border-gray-300 px-4 py-2">22</td>
              <td className="border border-gray-300 px-4 py-2">charlie@example.com</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default TablePage;