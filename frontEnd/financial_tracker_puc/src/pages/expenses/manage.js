import { useState, useEffect } from "react";
import axios from "axios";
import TransactionTable from "@/components/TransactionTable";
import TransactionEditor from "@/components/TransactionEditor";
import AddTransactionForm from "@/components/AddTransactionForm";

export default function ExpenseManagement() {
  const [data, setData] = useState([]);
  const [selectedTransaction, setSelectedTransaction] = useState(null);
  const [showAddTransaction, setShowAddTransaction] = useState(false);

  const fetchTransactions = async () => {
    try {
      const res = await axios.get("/api/pending_transactions", { withCredentials: true });
      setData(res.data);
    } catch (err) {
      console.error("Error fetching transactions:", err);
    }
  };

  useEffect(() => {
    fetchTransactions();
  }, []);

  const handleRowClick = (id) => {
    const selected = data.find(tx => tx.transaction_id === id);
    setSelectedTransaction(selected);
  };

  return (
    <div className="flex items-start gap-6 p-4">
      <div className="flex-grow">
        <TransactionTable
          data={data}
          onRowClick={handleRowClick}
          selectedId={selectedTransaction?.transaction_id}
        />
      </div>

      {selectedTransaction && (
        <TransactionEditor
          transaction={selectedTransaction}
          onClose={() => setSelectedTransaction(null)}
          refreshData={fetchTransactions}
        />
      )}

      {showAddTransaction && (
        <AddTransactionForm
          onClose={() => setShowAddTransaction(false)}
          refreshData={fetchTransactions}
        />
      )}
      <button
        onClick={() => setShowAddTransaction(true)}
        className="bg-blue-500 text-white px-4 py-2 rounded shadow hover:bg-blue-600 transition"
      >
        Add Transaction
      </button>
      
    </div>
  );
}