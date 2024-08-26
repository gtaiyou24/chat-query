"use client";

import PromptForm from "@/components/analytics/prompt-form";
import ChatMessages from "@/components/analytics/chat-messages";
import {useState} from "react";
import {ChatMessage, Field} from "@/lib/types";
import chatCompletion from "@/components/analytics/chat-completion";


export default function Chat() {
    const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
    const onSubmit = (message: string) => {
        const lastMessage: ChatMessage = { role: "user", content: message };
        const fields: Field[] = [];
        chatCompletion([...chatMessages, lastMessage], fields)
            .then((res) => {
                setChatMessages([...chatMessages, lastMessage, res.choices[0].message])
            })
            .catch((err) => {})
    };
    const onClear = () => setChatMessages([]);

    return (
        <div className="flex flex-col space-between">
            {chatMessages.length !== 0 && <ChatMessages
                messages={chatMessages}
                onDelete={(message, mIndex) => {
                    if (message.role === "user") {
                        setChatMessages((c) => {
                            const newChat = [...c];
                            newChat.splice(mIndex, 2);
                            return newChat;
                        });
                    } else if (message.role === 'assistant') {
                        setChatMessages((c) => {
                            const newChat = [...c];
                            newChat.splice(mIndex - 1, 2);
                            return newChat;
                        });
                    }
                }}
            />}
            <PromptForm onSubmit={onSubmit} onClear={onClear} />
        </div>
    );
}