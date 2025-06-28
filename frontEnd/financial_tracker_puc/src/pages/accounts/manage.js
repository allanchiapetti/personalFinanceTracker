import { useState, useEffect } from "react";
import axios from "axios";
import Account from "@/components/Account";

export default function AccountManager({ accounts }) {
  const [data, setData] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [editedBalance, setEditedBalance] = useState("");

  const handleUpdate = async (account_id) => {try {
    await fetch(`/api/update_account`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({"account_id": account_id,
			                "balance": editedBalance}),
    });

    fetchAccounts(); // Refresh accounts after update
    setSelectedId(null);
    setEditedBalance("");
  } catch (err) {
    console.error(err);
  }};

  const fetchAccounts = async () => {
    try {
      const res = await axios.get("/api/user_accounts", { withCredentials: true });
      setData(res.data);
    } catch (err) {
      console.error("Error fetching accounts:", err);
    }
  };

  useEffect(() => {
    fetchAccounts();
  }, []);
  
    const checkingAndSavings = data.filter(
        (acc) => acc.account_type === "Checking" || acc.account_type === "Savings"
    );
    
    const creditCards = data.filter((acc) => acc.account_type === "Credit Card");


  return (
   <div className="flex flex-col lg:flex-row gap-6 p-4">
  {/* Column 1: Checking & Savings */}
  <div className="flex-1 space-y-4">
    <h3 className="text-xl font-semibold text-gray-700">Bank Accounts</h3>
    {checkingAndSavings.map((account) => (
      <div key={account.account_id}>
        <Account account={account} onSelect={setSelectedId} />
        {selectedId === account.account_id && (
          <div className="mt-2">
            <input
              type="number"
              value={editedBalance}
              onChange={(e) => setEditedBalance(e.target.value)}
              placeholder={`Balance: ${account.balance}`}
              className="border px-2 py-1 rounded text-sm w-full"
            />
            <button
              onClick={() => handleUpdate(account.account_id)}
              className="mt-2 bg-blue-500 text-white px-3 py-1 rounded text-sm hover:bg-blue-600"
            >
              Save
            </button>
          </div>
        )}
      </div>
    ))}
  </div>

  {/* Column 2: Credit Cards */}
  <div className="flex-1 space-y-4">
    <h3 className="text-xl font-semibold text-gray-700">Credit Cards</h3>
    {creditCards.map((account) => (
      <div key={account.account_id}>
        <Account account={account} onSelect={setSelectedId} />
        {selectedId === account.account_id && (
          <p className="text-sm text-gray-500 italic mt-2">
            Balance updates for credit cards are not allowed.
          </p>
        )}
      </div>
    ))}
  </div>
</div>  );
}