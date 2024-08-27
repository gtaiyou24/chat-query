import {MemberTable} from "@/components/member/member-table";
import {columns} from "@/components/member/columns";
import {getMembers} from "@/lib/api";
import {auth} from "@/lib/auth";
import {notFound} from "next/navigation";


export default async function MembersPage() {
    const session = await auth();
    if (!session) notFound();
    const members = await getMembers(session.currentProject?.tenantId ?? session.user.tenants[0].id);
    return (
        <div className="container mx-auto mt-8">
            <MemberTable columns={columns} data={members} />
        </div>
    );
}