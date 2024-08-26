import Navbar from "../../components/layout/dashboard/navbar";
import Sidebar from "@/components/layout/dashboard/sidebar";


export default function DashboardLayout({ children }: { children: React.ReactNode }) {
    return (
        <>
            <Sidebar />
            <div className="flex flex-col sm:gap-4 sm:py-4 sm:pl-14">
                <Navbar />
                <main className="grid flex-1 items-start gap-2 p-4 sm:px-6 sm:py-0 md:gap-4">
                    {children}
                </main>
            </div>
        </>
    );
}
