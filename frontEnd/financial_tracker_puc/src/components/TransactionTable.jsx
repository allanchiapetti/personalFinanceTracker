import React, { useState } from 'react';

export default function TransactionTable({ data }) {
  const [selectedId, setSelectedId] = useState(null);

const handleRowClick = (id) => {
  setSelectedId(prevId => (prevId === id ? null : id));
};

  return (
    <div className="flex justify-left">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200 border border-gray-300 shadow-sm">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-2 text-left text-sm font-semibold text-gray-700">Date</th>
              <th className="px-4 py-2 text-left text-sm font-semibold text-gray-700">Description</th>
              <th className="px-4 py-2 text-left text-sm font-semibold text-gray-700">Amount ($)</th>
              <th className="px-4 py-2 text-left text-sm font-semibold text-gray-700">Type</th>
              <th className="px-4 py-2 text-left text-sm font-semibold text-gray-700">Category</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200 bg-white">
            {data.map((item) => (
              <tr
                key={item.transaction_id}
                onClick={() => handleRowClick(item.transaction_id)}
                className={`hover:bg-gray-100 cursor-pointer ${
                  selectedId === item.transaction_id ? 'bg-blue-100' : ''
                }`}
              >
                <td className="px-2 py-2 text-xs text-gray-700 w-32 truncate">
                  {new Date(item.transaction_date).toLocaleString()}
                </td>
                <td className="px-4 py-2 text-sm text-gray-800 w-32 truncate">{item.description}</td>
                <td className="px-4 py-2 text-sm text-gray-800 w-32 truncate">
                  {parseFloat(item.amount).toFixed(2)}
                </td>
                <td className="px-4 py-2 text-sm w-32">
                  <span
                    className={`inline-block px-2 py-1 text-xs font-medium rounded-full 
                      ${item.transaction_type === 'Debit'
                        ? 'bg-red-100 text-red-700'
                        : 'bg-green-100 text-green-700'}`}
                  >
                    {item.transaction_type}
                  </span>
                </td>
                <td className="px-4 py-2 text-sm text-gray-800">{item.category}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}