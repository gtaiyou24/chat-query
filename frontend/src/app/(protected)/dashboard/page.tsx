"use client";

import React from 'react';
import { VegaLite } from 'react-vega';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const salesData = [
    { month: 'Jan', sales: 20 },
    { month: 'Feb', sales: 35 },
    { month: 'Mar', sales: 40 },
    { month: 'Apr', sales: 55 },
    { month: 'May', sales: 60 },
    { month: 'Jun', sales: 75 },
    { month: 'Jul', sales: 80 },
    { month: 'Aug', sales: 100 },
    { month: 'Sep', sales: 90 },
    { month: 'Oct', sales: 85 },
    { month: 'Nov', sales: 80 },
    { month: 'Dec', sales: 95 },
];

const userActivityData = [
    { day: 'Mon', active: 100 },
    { day: 'Tue', active: 120 },
    { day: 'Wed', active: 150 },
    { day: 'Thu', active: 140 },
    { day: 'Fri', active: 160 },
    { day: 'Sat', active: 180 },
    { day: 'Sun', active: 200 },
];

const salesChartSpec = {
    width: 'container',
    height: 300,
    data: { values: salesData },
    mark: 'line',
    encoding: {
        x: { field: 'month', type: 'ordinal', title: '月' },
        y: { field: 'sales', type: 'quantitative', title: '売上高（万円）' },
        tooltip: [
            { field: 'month', type: 'ordinal', title: '月' },
            { field: 'sales', type: 'quantitative', title: '売上高（万円）' },
        ],
    },
};

const userActivityChartSpec = {
    width: 'container',
    height: 300,
    data: { values: userActivityData },
    mark: 'bar',
    encoding: {
        x: { field: 'day', type: 'ordinal', title: '曜日' },
        y: { field: 'active', type: 'quantitative', title: 'アクティブユーザー数' },
        tooltip: [
            { field: 'day', type: 'ordinal', title: '曜日' },
            { field: 'active', type: 'quantitative', title: 'アクティブユーザー数' },
        ],
    },
};

export default function DashboardPage() {
    return (
        <div className="p-4 space-y-4">
            <h1 className="text-2xl font-bold mb-4">ダッシュボード</h1>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Card>
                    <CardHeader>
                        <CardTitle>月間売上高推移</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <VegaLite spec={salesChartSpec} />
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader>
                        <CardTitle>曜日別アクティブユーザー数</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <VegaLite spec={userActivityChartSpec} />
                    </CardContent>
                </Card>
            </div>
            <Card>
                <CardHeader>
                    <CardTitle>概要</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
                        <div className="bg-blue-100 p-4 rounded-lg">
                            <h3 className="font-semibold text-blue-800">総売上高</h3>
                            <p className="text-2xl font-bold">¥76,500,000</p>
                        </div>
                        <div className="bg-green-100 p-4 rounded-lg">
                            <h3 className="font-semibold text-green-800">新規ユーザー</h3>
                            <p className="text-2xl font-bold">1,234</p>
                        </div>
                        <div className="bg-yellow-100 p-4 rounded-lg">
                            <h3 className="font-semibold text-yellow-800">平均滞在時間</h3>
                            <p className="text-2xl font-bold">15分</p>
                        </div>
                        <div className="bg-purple-100 p-4 rounded-lg">
                            <h3 className="font-semibold text-purple-800">コンバージョン率</h3>
                            <p className="text-2xl font-bold">3.5%</p>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
};