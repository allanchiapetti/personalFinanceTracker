"use client"
import { useSession } from 'next-auth/react';
import { useEffect, useState } from 'react';
import axios from 'axios';
import TransactionTable from '@/components/TransactionTable'; 

export default function ExpenseManagement() {
  const { data: session } = useSession();
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get('/api/transactions', { withCredentials: true })
      .then((res) => setData(res.data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Pending Transactions</h2>
      <TransactionTable data={data} />
    </div>
  );
}
