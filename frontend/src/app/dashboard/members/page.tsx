import {MemberTable} from "@/components/member/member-table";
import {columns} from "@/components/member/columns";
import {getMembers} from "@/lib/api";


export default async function MembersPage() {
    const members = await getMembers("030a4554-de1d-4d66-96d3-e2fff67e5143");
    return (
        <div className="container mx-auto mt-8">
            <MemberTable columns={columns} data={members} />
        </div>
    );
}