'use client';

import { useState, useEffect } from 'react';

interface Transaction {
  id: string;
  date: string;
  description: string;
  amount: number;
  category: string;
  merchant?: string;
  method?: string;
  currency: string;
  running_balance?: number;
}

export default function TransactionsPage() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [filterDays, setFilterDays] = useState(90);

  const generateTransactions = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/api/transactions/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          start_date: '2025-05-01', 
          months: 3,
          initial_balance: 2500.0
        })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setTransactions(data.transactions || []);
      console.log('Generated transactions:', data.summary);
    } catch (err) {
      setError(`Failed to generate transactions: ${err}`);
      console.error('Generate error:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadExistingTransactions = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/api/transactions');
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setTransactions(data || []);
    } catch (err) {
      setError(`Failed to load transactions: ${err}`);
      console.error('Load error:', err);
    } finally {
      setLoading(false);
    }
  };

  const filterTransactions = (days: number) => {
    setFilterDays(days);
  };

  // Filter transactions based on selected days
  const displayedTransactions = transactions.filter((tx) => {
    const txDate = new Date(tx.date);
    const now = new Date();
    const diffTime = now.getTime() - txDate.getTime();
    const diffDays = diffTime / (1000 * 3600 * 24);
    return diffDays <= filterDays;
  });

  // Load existing transactions on component mount
  useEffect(() => {
    loadExistingTransactions();
  }, []);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6">Transaction History</h1>
      
      {/* Controls */}
      <div className="flex flex-wrap gap-3 mb-6">
        <button
          className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded disabled:opacity-50 disabled:cursor-not-allowed"
          onClick={generateTransactions}
          disabled={loading}
        >
          {loading ? 'Generating...' : 'Generate New Transactions'}
        </button>
        
        <button
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded disabled:opacity-50 disabled:cursor-not-allowed"
          onClick={loadExistingTransactions}
          disabled={loading}
        >
          Refresh
        </button>
        
        <div className="flex gap-2">
          {[30, 60, 90].map((days) => (
            <button
              key={days}
              className={`px-3 py-2 rounded border transition-colors ${
                filterDays === days 
                  ? 'bg-gray-200 border-gray-400' 
                  : 'bg-white border-gray-300 hover:bg-gray-50'
              }`}
              onClick={() => filterTransactions(days)}
            >
              Last {days} days
            </button>
          ))}
        </div>
      </div>

      {/* Status Messages */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}
      
      {loading && (
        <div className="text-center py-4">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p className="mt-2">Loading transactions...</p>
        </div>
      )}

      {/* Transaction Summary */}
      {transactions.length > 0 && (
        <div className="bg-gray-50 p-4 rounded-lg mb-4">
          <p className="text-sm text-gray-600">
            Showing {displayedTransactions.length} of {transactions.length} transactions
            {filterDays < 90 && ` (filtered to last ${filterDays} days)`}
          </p>
        </div>
      )}

      {/* Transactions Table */}
      {displayedTransactions.length > 0 ? (
        <div className="overflow-y-auto max-h-[70vh] border rounded-lg shadow">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="sticky top-0 bg-gray-100 z-10">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Date
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Description
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Category
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Amount
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Balance
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-100">
              {displayedTransactions.map((tx) => (
                <tr key={tx.id} className="hover:bg-gray-50">
                  <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                    {new Date(tx.date).toLocaleDateString('en-CA')}
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-700">
                    {tx.description}
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-500">
                    {tx.category}
                  </td>
                  <td className={`px-4 py-3 whitespace-nowrap text-sm font-semibold ${
                    tx.amount >= 0 ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {tx.amount.toLocaleString('en-CA', { 
                      style: 'currency', 
                      currency: tx.currency || 'CAD' 
                    })}
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-700">
                    {tx.running_balance?.toLocaleString('en-CA', { 
                      style: 'currency', 
                      currency: tx.currency || 'CAD' 
                    })}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        !loading && (
          <div className="text-center py-8 text-gray-500">
            <p>No transactions found. Click "Generate New Transactions" to create sample data.</p>
          </div>
        )
      )}
    </div>
  );
}
