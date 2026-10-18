import { NextResponse } from 'next/server';

export function middleware(request) {
  if (request.cookies.get('lab-session')?.value !== process.env.LAB_SESSION_TOKEN) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }
  return NextResponse.next();
}

export const config = { matcher: ['/api/private/:path*'] };
