import {APP_NAME} from "@/lib/constants";
import Image from "next/image";


export default function Logo({
    width,
    height
}: {
    width: number;
    height: number;
}) {
    return (
        <>
            <Image src='/logo-dark.png' className={"rounded-lg hidden dark:block"} alt={APP_NAME} width={width} height={height} />
            <Image src='/logo-light.png' className={"rounded-lg block dark:hidden"} alt={APP_NAME} width={width} height={height} />
        </>
    );
}