import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const BACKEND = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
    
    // Proxy the generate request to FastAPI backend
    const response = await fetch(`${BACKEND}/transactions/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    
    if (!response.ok) {
      throw new Error(`Backend responded with status: ${response.status}`);
    }
    
    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
    
  } catch (err) {
    console.error('Generate transactions API error:', err);
    return NextResponse.json(
      { error: 'Failed to generate transactions', details: String(err) },
      { status: 500 }
    );
  }
}
