export default function Account({ account, onSelect, onDelete }) {
  const { account_id, account_name, account_type, balance, institution } = account;

  const typeColors = {
    "Checking": "border-green-500",
    "Savings": "border-blue-500",
    "Credit Card": "border-red-500"
  };

  const borderClass = typeColors[account_type] || "border-gray-300";

  return (
    <div
      className={`relative border-2 ${borderClass} p-4 rounded shadow hover:shadow-md transition-all`}
    >
      {/* Red X Button */}
      <button
        onClick={() => onDelete(account_id)}
        className="absolute top-2 right-2 text-red-500 hover:text-red-700 text-lg font-bold focus:outline-none"
        title="Delete Account"
      >
        &times;
      </button>

      {/* Card Content */}
      <div onClick={() => onSelect(account_id)} className="cursor-pointer">
        <h2 className="font-bold text-lg">{account_name}</h2>
        <p className="text-sm text-gray-600">{account_type}</p>
        <p className="text-sm">Institution: {institution}</p>
        <p className="text-sm mt-1">Balance: ${parseFloat(balance).toFixed(2)}</p>
      </div>
    </div>
  );
}