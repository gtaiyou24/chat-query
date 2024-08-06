"use client";

import {Accordion, AccordionContent, AccordionItem, AccordionTrigger} from "@/components/ui/accordion";
import {FilterListItem as Item, FilterListItem} from "@/lib/types";
import {useSearchParams} from "next/navigation";
import {useCallback} from "react";
import {Badge} from "@/components/ui/badge";
import FilterCheckbox from "@/components/form/filter-checkbox";


function FilterAccordionItem({ item }: { item: Item; }) {
    const readonlyURLSearchParams = useSearchParams();
    const countChecked = useCallback((handle: string): number => {
        return readonlyURLSearchParams.getAll(handle).length;
    }, [readonlyURLSearchParams]);
    return (
        <AccordionItem value={`${item.handle}`} className="px-2 lg:px-0">
            <AccordionTrigger className="hover:no-underline">
                <div className="flex gap-2">
                    {item.name}
                    <Badge variant="secondary">{countChecked(item.handle)}</Badge>
                </div>
            </AccordionTrigger>
            <AccordionContent className="grid gap-2">
                {item.options.map((option, optionIndex) => (
                    <FilterCheckbox
                        key={`${item.handle}-${option}`}
                        id={`${item.handle}-${option}`}
                        handle={item.handle}
                        name={option} />
                ))}
            </AccordionContent>
        </AccordionItem>
    );
}


export default function FilterAccordion({ list }: { list: FilterListItem[]; }) {
    return (
        <Accordion type="single" collapsible>
            {list.map((item, index) => <FilterAccordionItem key={item.handle} item={item} />)}
        </Accordion>
    );
}