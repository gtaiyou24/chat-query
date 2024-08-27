"use client";

import PromptForm from "@/components/chat/prompt-form";
import ChatMessages from "@/components/chat/chat-messages";
import {useEffect, useState} from "react";
import {ChatMessage, Dataset, DSItem} from "@/lib/types";
import chatCompletion from "@/components/chat/chat-completion";
import {toast} from "sonner";
import SelectDataset from "@/components/chat/select-dataset";
import {Button} from "@/components/ui/button";
import {matchQuote} from "@/lib/utils";
import DataTable from "@/components/data-table/data-table";
import {produce} from "immer";


const EXAMPLE_DATASETS: DSItem[] = [
    {
        key: "cars",
        name: "車",
        url: "/datasets/cars.json",
        type: "demo",
    },
    {
        key: "students",
        name: "学生名簿",
        url: "/datasets/students.json",
        type: "demo",
    },
];


export default function Chat() {
    // データセット
    const [dsItems, setDsItems] = useState<DSItem[]>(EXAMPLE_DATASETS);
    const [datasetKey, setDatasetKey] = useState<string>(EXAMPLE_DATASETS[0].key);
    const [dataset, setDataset] = useState<Dataset | null>(null);

    // チャット
    const [pivotKey, setPivotKey] = useState<string>("viz");
    const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);

    useEffect(() => {
        const currentDatasetInfo =
            dsItems.find((dsItem) => dsItem.key === datasetKey) ?? dsItems[0];
        if (currentDatasetInfo.type === "demo") {
            fetch(currentDatasetInfo.url)
                .then((res) => res.json())
                .then((res) => {
                    setDataset(res);
                })
                .catch(() => {
                    toast("データセットが見つかりませんでした。");
                });
        } else {
            setDataset(currentDatasetInfo.dataset);
        }
    }, [datasetKey, dsItems]);

    const onSubmit = (message: string) => {
        const lastMessage: ChatMessage = { role: "user", content: message };
        const fields = dataset?.fields ?? [];
        chatCompletion([...chatMessages, lastMessage], fields)
            .then((res) => {
                if (res.choices.length > 0) {
                    const spec = matchQuote(res.choices[0].message.content, "{", "}");
                    if (spec) {
                        setChatMessages([...chatMessages, lastMessage, res.choices[0].message]);
                    } else {
                        setChatMessages([...chatMessages, lastMessage, {
                            role: 'assistant',
                            content: 'There is no relative visualization for your query. Please check the dataset and try again.',
                        }]);
                        // throw new Error(
                        //     "No visualization matches your instruction.\n" +
                        //         res.choices[0].message.content
                        // );
                    }
                }
            })
            .catch((err) => {
                toast(err.message);
            })
    };
    const onClear = () => setChatMessages([]);
    const deleteMessage = (message: ChatMessage, mIndex: number) => {
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
    }

    return (
        <>
            <div className="flex gap-4 items-end my-2">
                <div>
                    <SelectDataset
                        items={dsItems}
                        selectedKey={datasetKey}
                        onChange={(dsKey) => setDatasetKey(dsKey)}
                    />
                </div>
                <Button>CSVデータをアップロード</Button>
                <div className="ml-4">
                    <span className="isolate inline-flex rounded-md shadow-sm">
                        <button
                            type="button"
                            className={`relative inline-flex items-center rounded-l-md px-3 py-2 text-sm font-semibold text-gray-900 dark:text-gray-50 ring-1 ring-inset ring-gray-300 dark:ring-gray-500 hover:bg-indigo-500 hover:text-white focus:z-10 ${
                                pivotKey === "viz"
                                    ? "bg-indigo-600 border-indigo-600 text-white"
                                    : ""
                            }`}
                            onClick={() => {
                                setPivotKey("viz");
                            }}
                        >
                            チャット分析
                        </button>
                        <button
                            type="button"
                            className={`relative -ml-px inline-flex items-center rounded-r-md px-3 py-2 text-sm font-semibold text-gray-900 dark:text-gray-50 ring-1 ring-inset ring-gray-300 dark:ring-gray-500 hover:bg-indigo-500 hover:text-white focus:z-10 ${
                                pivotKey === "data"
                                    ? "bg-indigo-600 border-indigo-600 text-white"
                                    : ""
                            }`}
                            onClick={() => {
                                setPivotKey("data");
                            }}
                        >
                            データセット
                        </button>
                    </span>
                </div>
            </div>

            {pivotKey === "viz" && (
            <div className="flex flex-col space-between">
                {(dataset && chatMessages.length !== 0) && <ChatMessages
                    dataset={dataset}
                    messages={chatMessages}
                    onDelete={deleteMessage}
                />}
                <PromptForm onSubmit={onSubmit} onClear={onClear} />
            </div>
            )}
            {pivotKey === "data" && (
                <div>
                    {dataset && (
                        <DataTable
                            data={dataset.dataSource}
                            metas={dataset.fields}
                            onMetaChange={(fid, fIndex, meta) => {
                                const nextDataset = produce(
                                    dataset,
                                    (draft) => {
                                        draft.fields[fIndex] = {
                                            ...draft.fields[fIndex],
                                            ...meta,
                                        };
                                    }
                                );
                                setDataset(nextDataset);
                            }}
                        />
                    )}
                </div>
            )}
        </>
    );
}