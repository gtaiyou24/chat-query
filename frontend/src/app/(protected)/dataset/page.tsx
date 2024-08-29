import {Tabs, TabsContent, TabsList, TabsTrigger} from "@/components/ui/tabs";


export default function DatasetPage() {
    return (
        <div className="container mx-auto px-48">
            <div className="flex justify-between gap-4 my-8">
                <h1 className="text-2xl font-bold">データセット</h1>

            </div>
            <Tabs defaultValue="file" className="w-[400px]">
                <TabsList>
                    <TabsTrigger value="file">ファイル</TabsTrigger>
                    <TabsTrigger value="database">データベース</TabsTrigger>
                </TabsList>
                <TabsContent value="file">Make changes to your account here.</TabsContent>
                <TabsContent value="database">Change your password here.</TabsContent>
            </Tabs>
        </div>
    );
}