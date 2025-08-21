import { NextRequest, NextResponse } from 'next/server';

export async function GET(req: NextRequest) {
  try {
    const BACKEND = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
    
    // Extract query parameters
    const url = new URL(req.url);
    const startDate = url.searchParams.get('start_date') || '2025-05-01';
    const months = url.searchParams.get('months') || '3';
    
    const response = await fetch(`${BACKEND}/transactions?start_date=${startDate}&months=${months}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });
    
    if (response.ok) {
      const data = await response.json();
      return NextResponse.json(data);
    } else {
      throw new Error(`Backend responded with status: ${response.status}`);
    }
    
  } catch (err) {
    console.error('Transaction API error:', err);
    return NextResponse.json(
      { error: 'Failed to fetch transactions', details: String(err) },
      { status: 500 }
    );
  }
}

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const BACKEND = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
    
    const response = await fetch(`${BACKEND}/transactions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    
    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
    
  } catch (err) {
    return NextResponse.json(
      { error: 'Failed to create transaction', details: String(err) },
      { status: 500 }
    );
  }
}
