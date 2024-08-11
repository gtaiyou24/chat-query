import { Button } from '@/components/ui/button';
import { auth, signOut } from '@/lib/auth';
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger
} from '@/components/ui/dropdown-menu';
import Link from 'next/link';
import {Avatar, AvatarFallback} from "@/components/ui/avatar";

export async function UserNav() {
    const session = await auth();
    const user = session?.user;

    return (
        <DropdownMenu>
            <DropdownMenuTrigger className="ml-auto" asChild>
                <Button
                    variant="outline"
                    size="icon"
                    className="overflow-hidden rounded-full"
                >
                    <Avatar className="h-8 w-8">
                        {/*<AvatarImage*/}
                        {/*    src={session.user?.image ?? ""}*/}
                        {/*    alt={session.user?.email ?? ""}*/}
                        {/*/>*/}
                        <AvatarFallback>{session!.user?.name?.substring(0, 2)}</AvatarFallback>
                    </Avatar>
                </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
                <DropdownMenuLabel>My Account</DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem>Settings</DropdownMenuItem>
                <DropdownMenuItem>Support</DropdownMenuItem>
                <DropdownMenuSeparator />
                {user ? (
                    <DropdownMenuItem>
                        <form
                            action={async () => {
                                'use server';
                                await signOut();
                            }}
                        >
                            <button type="submit">Sign Out</button>
                        </form>
                    </DropdownMenuItem>
                ) : (
                    <DropdownMenuItem>
                        <Link href="/login">Sign In</Link>
                    </DropdownMenuItem>
                )}
            </DropdownMenuContent>
        </DropdownMenu>
    );
}