import { useState, useEffect } from "react";

export default function TransactionEditor({ transaction, onClose, refreshData}) {
  const [form, setForm] = useState(transaction);
  const [fadingOut, setFadingOut] = useState(false);

  // Sync form state when transaction prop changes
  useEffect(() => {
    setForm(transaction);
  }, [transaction]);

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleBlur = () => {
    setForm((prev) => ({
        ...prev,
        amount: Number(prev.amount).toFixed(2),
    }));
    
    setForm((prev) => ({
        ...prev,
        balance: prev.balance < prev.amount ? Number(prev.balance).toFixed(2) : Number(prev.amount).toFixed(2),
    }));
    };

const handleSubmit = async (e) => {
  e.preventDefault();
  try {
    await fetch(`/api/update_transaction`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });

    setFadingOut(true); // Trigger the fade-out animation

    setTimeout(() => {
      refreshData(); // Refresh table
      onClose();     // Close editor after fade
    }, 300); // 
  } catch (err) {
    console.error(err);
  }
};

  return (
    <div className={`transition-opacity duration-300 ${fadingOut ? 'opacity-0' : 'opacity-100'}`}>
        <div className="w-80 bg-white border border-gray-300 shadow-md p-4 rounded">
        <h3 className="text-lg font-semibold mb-4 text-black">Edit Transaction</h3>
        <form onSubmit={handleSubmit} className="flex flex-col gap-3 text-black">
            <input
            name="description"
            value={form.description || ""}
            onChange={handleChange}
            placeholder="Description"
            className="border px-3 py-1 rounded"
            />
            <input
            name="amount"
            value={form.amount || ""}
            onChange={handleChange}
            onBlur={handleBlur}
            placeholder="Amount"
            type="number"
            step="0.01"
            min="0"
            className="border px-3 py-1 rounded"
            />
            <input
            name="balance"
            value={form.balance || ""}
            onChange={handleChange}
            onBlur={handleBlur}
            placeholder="Balance"
            type="number"
            step="0.01"
            min="0"
            className="border px-3 py-1 rounded"
            />
            <input
            name="category"
            value={form.category || ""}
            onChange={handleChange}
            placeholder="Category"
            className="border px-3 py-1 rounded"
            />
            <select
            name="transaction_type"
            value={form.transaction_type || ""}
            onChange={handleChange}
            className="border px-3 py-1 rounded"
            >
            <option value="Debit">Debit</option>
            <option value="Credit">Credit</option>
            </select>
            <button
            type="submit"
            className="bg-blue-500 text-white px-4 py-1 rounded hover:bg-blue-600"
            >
            Save
            </button>
            <button
            type="button"
            onClick={onClose}
            className="text-sm text-gray-500 mt-1"
            >
            Cancel
            </button>
        </form>
        </div>
    </div>
  );
}