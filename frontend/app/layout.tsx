import "./globals.css";
import type { ReactNode } from "react";

export const metadata = {
  title: "Income statement",
  description: "Northwind Coffee Roasters P&L",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
