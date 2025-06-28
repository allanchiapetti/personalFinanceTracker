import { useState, useEffect } from "react";

export default function AddTransactionForm({ onClose, refreshData }) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [form, setForm] = useState({
    account_id: "",
    description: "",
    amount: "",
    category: "",
    transaction_type: "Debit",
    transaction_date: new Date().toISOString().split("T")[0], // Default to today
  });

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const [accounts, setAccounts] = useState([]);

  useEffect(() => {
    const fetchAccounts = async () => {
      try {
        const res = await fetch("/api/user_accounts", { credentials: "include" }); // or axios if you're using that
        const data = await res.json();
        setAccounts(data);
      } catch (err) {
        console.error("Failed to fetch accounts:", err);
      }
    };

    fetchAccounts();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (isSubmitting) return; // Prevent multiple submissions
    setIsSubmitting(true);
    try {
      await fetch("/api/create_transaction", {
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
      amount: Number(prev.amount).toFixed(2),
    }));
  };


  return (
    <div className="w-80 bg-white border border-gray-300 shadow-md p-4 rounded-md text-black">
      <h3 className="text-lg font-semibold mb-4">Add Transaction</h3>
      <form onSubmit={handleSubmit} className="flex flex-col gap-3">
        <input
          name="transaction_date"
          type="date"
          value={form.transaction_date}
          onChange={handleChange}
          className="border px-3 py-1 rounded"
          required
        />
        <select
          name="account_id"
          value={form.account_id}
          onChange={handleChange}
          className="border px-3 py-1 rounded"
          required
        >
          <option value="">Select Account</option>
          {accounts.map((acct) => (
            <option key={acct.account_id} value={acct.account_id}>
              {acct.account_name} — {acct.account_type}
            </option>
          ))}
        </select>
        <input
          name="description"
          value={form.description}
          onChange={handleChange}
          placeholder="Description"
          required
          className="border px-3 py-1 rounded"
        />
        <input
          name="amount"
          value={form.amount}
          onChange={handleChange}
          onBlur={handleBlur}
          placeholder="Amount"
          min="0.01"
          type="number"
          step="0.01"
          required
          className="border px-3 py-1 rounded"
        />
        <input
          name="category"
          value={form.category}
          onChange={handleChange}
          placeholder="Category"
          required
          className="border px-3 py-1 rounded"
        />
        <select
          name="transaction_type"
          value={form.transaction_type}
          onChange={handleChange}
          required
          className="border px-3 py-1 rounded"
        >
          <option value="Debit">Debit</option>
          <option value="Credit">Credit</option>
        </select>
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