import type { Metadata } from "next";
import "../globals.css";

export const metadata: Metadata = {
  title: "DARSI Admin Dashboard",
  description: "Hospital customer service administration",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
