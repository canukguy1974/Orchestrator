// apps/web/frontend/src/pages/transactions.tsx
import React, { useState, useEffect } from 'react';

interface Transaction {
  id: string;
  date: string;
  description: string;
  amount: number;
  category: string;
  merchant?: string;
  method?: string;
  currency: string;
  runningBalance?: number;
}

const TransactionPage = () => {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [filterDays, setFilterDays] = useState(90);

  const generate = async () => {
    const res = await fetch('/api/transactions/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ start_date: '2025-05-01', months: 3 })
    });
    const data = await res.json();
    setTransactions(data.transactions);
  };

  const filter = (days: number) => {
    setFilterDays(days);
  };

  const displayed = transactions.filter((tx) => {
    const txDate = new Date(tx.date);
    const now = new Date();
    const diff = (now.getTime() - txDate.getTime()) / (1000 * 3600 * 24);
    return diff <= filterDays;
  });

  return (
    <div className="p-4">
      <div className="flex gap-3 mb-4">
        <button
          className="bg-green-600 text-white px-4 py-2 rounded"
          onClick={generate}
        >
          Generate Transactions
        </button>
        {[30, 60, 90].map((d) => (
          <button
            key={d}
            className={`px-3 py-2 rounded border ${filterDays === d ? 'bg-gray-200' : 'bg-white'}`}
            onClick={() => filter(d)}
          >
            Last {d} days
          </button>
        ))}
      </div>
      <div className="overflow-y-auto max-h-[70vh] border rounded">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="sticky top-0 bg-gray-100">
            <tr>
              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
                Date
              </th>
              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
                Description
              </th>
              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
                Category
              </th>
              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
                Amount
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-100">
            {displayed.map((tx) => (
              <tr key={tx.id}>
                <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-700">
                  {new Date(tx.date).toLocaleDateString('en-CA')}
                </td>
                <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-700">
                  {tx.description}
                </td>
                <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-700">
                  {tx.category}
                </td>
                <td
                  className={`px-4 py-2 whitespace-nowrap text-sm font-semibold ${
                    tx.amount >= 0 ? 'text-green-600' : 'text-red-600'
                  }`}
                >
                  {tx.amount.toLocaleString('en-CA', { style: 'currency', currency: 'CAD' })}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default TransactionPage;
