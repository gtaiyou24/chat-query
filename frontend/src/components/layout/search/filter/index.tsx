import {Suspense} from "react";
import {FilterListItem} from "@/lib/types";
import SearchInput from "@/components/form/search-input";
import FilterAccordion from "@/components/layout/search/filter/accordion";
import FilterDrawer from "@/components/layout/search/filter/drawer";

export default function FilterList({ list }: { list: FilterListItem[] }) {
    return (
        <nav>
            <ul className="hidden md:block">
                <Suspense fallback={null}>
                    <SearchInput />
                    <FilterAccordion list={list} />
                </Suspense>
            </ul>
            <ul className="md:hidden">
                <Suspense fallback={null}>
                    <SearchInput />
                    <FilterDrawer list={list} />
                </Suspense>
            </ul>
        </nav>
    );
}