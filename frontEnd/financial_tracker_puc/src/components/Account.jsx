export default function Account({ account, onSelect }) {
  const { account_id, account_name, account_type, balance, institution } = account;

  const typeColors = {
    "Checking": "border-green-500",
    "Savings": "border-blue-500",
    "Credit Card": "border-red-500"
  };

  const borderClass = typeColors[account_type] || "border-gray-300";

  return (
    <div
      className={`border-2 ${borderClass} p-4 rounded shadow hover:shadow-md cursor-pointer transition-all`}
      onClick={() => onSelect(account_id)}
    >
      <h2 className="font-bold text-lg">{account_name}</h2>
      <p className="text-sm text-gray-600">{account_type}</p>
      <p className="text-sm">Institution: {institution}</p>
      <p className="text-sm mt-1">Balance: ${parseFloat(balance).toFixed(2)}</p>
    </div>
  );
}