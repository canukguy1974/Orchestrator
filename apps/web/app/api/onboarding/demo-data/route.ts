import { NextRequest, NextResponse } from 'next/server';

const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:8000';

export async function POST() {
  try {
    const response = await fetch(`${API_BASE_URL}/onboarding/demo-data`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error creating demo data:', error);
    return NextResponse.json(
      { error: 'Failed to create demo data' },
      { status: 500 }
    );
  }
}
