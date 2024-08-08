import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import {clsx} from "clsx";
import Footer from "@/components/layout/footer";
import {Toaster} from "@/components/ui/toaster";
import Provider from "@/components/provider";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Analytics GPT",
  description: "ノーコードで分析できる GPT",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ja">
      <body className={clsx(inter.className, 'flex min-h-screen w-full flex-col')}>
        <Provider>
          <main className="flex-grow">
            {children}
          </main>
          <Footer />
          <Toaster />
        </Provider>
      </body>
    </html>
  );
}
