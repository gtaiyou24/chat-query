import {cn} from "@/lib/utils";


export default function Loading(props: React.ComponentProps<'div'>) {
    return (
        <div className="flex justify-center" aria-label="読み込み中">
            <div className={cn(props.className, "animate-spin h-4 w-4 border-2 border-accent rounded-full border-t-transparent")}></div>
        </div>
    );
}