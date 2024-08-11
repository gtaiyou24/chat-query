import Link from "next/link";
import Logo from "@/components/logo";
import {NavItem} from "@/components/layout/dashboard/nav-item";
import {Home, LineChart, Settings, Users2} from "lucide-react";
import ThemeToggle from "@/components/layout/dashboard/navbar/theme-toggle";
import {Tooltip, TooltipContent, TooltipTrigger} from "@/components/ui/tooltip";


export default function Sidebar() {
    return (
        <aside className="fixed inset-y-0 left-0 z-10 hidden w-14 flex-col border-r bg-background sm:flex">
            <nav className="flex flex-col items-center gap-4 px-2 sm:py-5">
                <Link
                    href="https://vercel.com/templates/next.js/admin-dashboard-tailwind-postgres-react-nextjs"
                    className="group flex h-9 w-9 shrink-0 items-center justify-center gap-2 rounded-full bg-primary text-lg font-semibold text-primary-foreground md:h-8 md:w-8 md:text-base"
                >
                    <Logo width={40} height={40} className="transition-all group-hover:scale-110" />
                    <span className="sr-only">Acme Inc</span>
                </Link>

                <NavItem href="#" label="ダッシュボード">
                    <Home className="h-5 w-5" />
                </NavItem>

                <NavItem href="/customers" label="メンバー">
                    <Users2 className="h-5 w-5" />
                </NavItem>

                <NavItem href="#" label="Analytics">
                    <LineChart className="h-5 w-5" />
                </NavItem>
            </nav>
            <nav className="mt-auto flex flex-col items-center gap-4 px-2 sm:py-5">
                <ThemeToggle />
                <Tooltip>
                    <TooltipTrigger asChild>
                        <Link
                            href="#"
                            className="flex h-9 w-9 items-center justify-center rounded-lg text-muted-foreground transition-colors hover:text-foreground md:h-8 md:w-8"
                        >
                            <Settings className="h-5 w-5" />
                            <span className="sr-only">Settings</span>
                        </Link>
                    </TooltipTrigger>
                    <TooltipContent side="right">Settings</TooltipContent>
                </Tooltip>
            </nav>
        </aside>
    );
}