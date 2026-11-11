import { NextResponse } from 'next/server';

export function middleware(request) {
  const expected = process.env.LAB_SESSION_TOKEN;
  const supplied = request.cookies.get('lab-session')?.value;
  if (typeof expected !== 'string' || !expected || typeof supplied !== 'string' || supplied !== expected) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }
  return NextResponse.next();
}

export const config = { matcher: ['/api/private/:path*'] };
