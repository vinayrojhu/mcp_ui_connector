import './globals.css';
import type { ReactNode } from 'react';
export const metadata = { title: 'Adaptive UI Connector', description: 'Locally controlled workflow automation' };
export default function RootLayout({ children }: { children: ReactNode }) { return <html lang="en"><body>{children}</body></html>; }
