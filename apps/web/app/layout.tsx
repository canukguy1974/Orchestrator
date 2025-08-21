import './globals.css';
import React from 'react';
import Link from 'next/link';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <nav className="bg-blue-600 text-white p-4">
          <div className="container mx-auto flex space-x-4">
            <Link href="/" className="hover:text-blue-200">
              Home
            </Link>
            <Link href="/transactions" className="hover:text-blue-200">
              Transactions
            </Link>
          </div>
        </nav>
        <main>{children}</main>
      </body>
    </html>
  );
}