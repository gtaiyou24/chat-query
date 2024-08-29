"use client";

import React, {useEffect, useState} from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import ReactVega from "@/components/vega/react-vega";
import {toast} from "sonner";
import {Dataset} from "@/lib/types";

export default function DashboardPage() {
    const [dataset, setDataset] = useState<Dataset | null>(null);

    useEffect(() => {
        fetch("/datasets/customers.json")
            .then((res) => res.json())
            .then((res) => {
                setDataset(res);
            })
            .catch(() => {
                toast("データセットが見つかりませんでした。");
            });
    }, []);

    return (
        <div className="p-6 space-y-6">
            <h1 className="text-3xl font-bold mb-6">ダッシュボード</h1>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <Card>
                    <CardHeader>
                        <CardTitle>総データセット数</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <p className="text-4xl font-bold">42</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader>
                        <CardTitle>アクティブユーザー</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <p className="text-4xl font-bold">128</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader>
                        <CardTitle>総分析回数</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <p className="text-4xl font-bold">1,024</p>
                    </CardContent>
                </Card>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-1 gap-6">
                <Card>
                    <CardHeader>
                        <CardTitle>購入者数の推移</CardTitle>
                    </CardHeader>
                    <CardContent>
                        {dataset && <ReactVega
                            spec={{
                                mark: "line",
                                encoding: {
                                    x: {
                                        field: "初回購入日",
                                        type: "temporal",
                                        title: "初回購入日"
                                    },
                                    y: {
                                        aggregate: "count",
                                        field: "顧客ID",
                                        type: "quantitative",
                                        title: "COUNT(顧客ID)"
                                    }
                                }
                            }}
                            data={dataset.dataSource ?? []} width={1500} />}
                    </CardContent>
                </Card>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <Card>
                    <CardHeader>
                        <CardTitle>購入回数</CardTitle>
                    </CardHeader>
                    <CardContent>
                        {dataset && <ReactVega
                            spec={{
                                mark: "bar",
                                encoding: {
                                    x: {
                                        field: "購入回数",
                                        bin: { maxbins: 20 },
                                        type: "quantitative",
                                        title: "BIN(購入回数)"
                                    },
                                    y: {
                                        aggregate: "count",
                                        type: "quantitative"
                                    }
                                }
                            }}
                            data={dataset.dataSource ?? []} width={300} />}
                    </CardContent>
                </Card>
            </div>
        </div>
    );
};