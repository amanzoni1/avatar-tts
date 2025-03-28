import type { Metadata } from "next";
import "./globals.css";
import GradientBackground from "@/components/GradientBackground/GradientBackground";
export const metadata: Metadata = {
  title: "AI Avatar Text-to-Speech",
  description: "An AI-powered avatar that speaks your text",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <GradientBackground />
        {children}
      </body>
    </html>
  );
}
