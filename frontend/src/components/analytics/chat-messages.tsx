"use client";

import {useEffect, useRef} from "react";
import {ChatMessage} from "@/lib/types";
import { TrashIcon, UserIcon } from "@heroicons/react/20/solid";
import { CpuChipIcon } from "@heroicons/react/24/outline";


export default function ChatMessages({
    messages,
    onDelete
}: {
    messages: ChatMessage[];
    onDelete?: (message: ChatMessage, mIndex: number) => void;
}) {
    const container = useRef<HTMLDivElement>(null);
    useEffect(() => {
        if (container.current) {
            container.current.scrollTop = container.current.scrollHeight;
        }
    }, [messages]);

    return (
        <div className="border-2 border-zinc-100 dark:border-zinc-800 overflow-y-auto" ref={container} style={{ maxHeight: "80vh" }}>
            {messages.map((message, index) => {
                if (message.role === 'assistant') {
                    return (
                        <div className="p-4 flex justify-top" key={index}>
                            <div className="grow-0">
                                <div className="inline-block h-10 w-10 rounded-full mx-4 bg-indigo-500 text-white flex items-center justify-center">
                                    <CpuChipIcon className="w-6" />
                                </div>
                            </div>
                            <div className="grow pl-8 overflow-x-auto">
                                <p>{message.content}</p>
                                {/*<DataTable*/}
                                {/*    data={dataset.dataSource}*/}
                                {/*    metas={dataset.fields}*/}
                                {/*    onMetaChange={() => {*/}
                                {/*        console.log("meta changed");*/}
                                {/*    }}*/}
                                {/*/>*/}
                            </div>
                        </div>
                    );
                }
                return (
                    <div className="p-4 bg-zinc-100 dark:bg-zinc-800 flex" key={index}>
                        <div className="grow-0">
                            <div className="inline-block h-10 w-10 rounded-full mx-4 bg-green-500 text-white flex items-center justify-center">
                                <UserIcon className="w-6" />
                            </div>
                        </div>
                        <div className="grow pl-8">
                            <p>{message.content}</p>
                        </div>
                        <div className="float-right">
                            <TrashIcon
                                className="w-4 text-gray-500 dark:text-gray-300 cursor-pointer hover:scale-125"
                                onClick={() => {
                                    onDelete && onDelete(message, index);
                                }}
                            />
                        </div>
                    </div>
                );
            })}
        </div>
    );
}