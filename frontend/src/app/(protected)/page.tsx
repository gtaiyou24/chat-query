import Chat from "@/components/chat/chat";
import {Button} from "@/components/ui/button";
import {PlusCircle} from "lucide-react";
import React from "react";


export default function HomePage() {
    return (
        <div className="p-6 space-y-6">
            <div className="flex justify-between">
                <h1 className="text-2xl font-bold">分析</h1>
                <Button>
                    <PlusCircle className="mr-2 h-4 w-4" /> データを追加
                </Button>
            </div>
            <Chat />
        </div>
    );
}