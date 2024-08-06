export default function AuthLayout({ children }: { children: React.ReactNode }) {
    return (
        <main className="h-full flex items-center justify-center min-h-screen">
            {children}
        </main>
    );
};