"use server";

import {ChatMessage, ChatResponse, Field} from "@/lib/types";

export default async function chatCompletion(
    messages: ChatMessage[],
    metas: Field[]
): Promise<ChatResponse> {
    const res = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            messages,
            metas
        }),
    });
    const result = (await res.json()) as {
        data: ChatResponse;
        success: boolean;
        message?: string;
    };
    if (result.success) {
        return result.data;
    } else {
        throw new Error(result.message ?? "Unknown error");
    }
}