import { useState, useEffect } from "react";

export default function AddTransactionForm({ onClose, refreshData }) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [form, setForm] = useState({
    institution: "",
    account_name: "",
    account_type: "",
    balance: ""
  });

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };


  const handleSubmit = async (e) => {
    e.preventDefault();
    if (isSubmitting) return; // Prevent multiple submissions
    setIsSubmitting(true);
    try {
      await fetch("/api/create_account", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      refreshData();
      onClose();
    } catch (err) {
      console.error(err);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleBlur = () => {
    setForm((prev) => ({
      ...prev,
      balance: Number(prev.balance).toFixed(2),
    }));
  };


  return (
    <div className="w-80 bg-white border border-gray-300 shadow-md p-4 rounded-md text-black">
      <h3 className="text-lg font-semibold mb-4">Add Transaction</h3>
      <form onSubmit={handleSubmit} className="flex flex-col gap-3">

        <input
          name="institution"
          value={form.institution}
          onChange={handleChange}
          placeholder="Institution"
          required
          className="border px-3 py-1 rounded"
        />
        <input
          name="account_name"
          value={form.account_name}
          onChange={handleChange}
          placeholder="Account Name"
          required
          className="border px-3 py-1 rounded"
        />
        <select
          name="account_type"
          value={form.account_type}
          onChange={handleChange}
          required
          className="border px-3 py-1 rounded"
        
        > <option value="" disabled>Select Account Type</option>
          <option value="Checking">Checking</option>
          <option value="Savings">Savings</option>
          <option value="Credit Card">Credit Card</option>
        </select>

        <input
          name="balance"
          value={form.balance}
          onChange={handleChange}
          onBlur={handleBlur}
          placeholder="Balance"
          min="0.01"
          type="number"
          step="0.01"
          required
          className="border px-3 py-1 rounded"
        />

        <button type="submit" className="bg-blue-500 text-white px-4 py-1 rounded hover:bg-blue-700">
          Save
        </button>
        <button type="button" onClick={onClose} className="text-sm text-gray-500 mt-1">
          Cancel
        </button>
      </form>
    </div>
  );
}