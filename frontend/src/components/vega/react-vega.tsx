import { useEffect, useRef } from "react";
import embed, { vega } from 'vega-embed';
import {Row} from "@/lib/types";
import {useCurrentMediaTheme, VegaTheme} from "@/components/vega/theme";


export default function ReactVega({
    spec,
    data
}: {
    spec: any;
    data?: Row[]
}) {
    const container = useRef<HTMLDivElement>(null);

    const theme = useCurrentMediaTheme();

    useEffect(() => {
        if (container.current && data) {
            spec.data = {
                name: 'dataSource'
            }
            embed(container.current, spec, { actions: false, config: VegaTheme[theme] }).then(res => {
                res.view.change('dataSource', vega.changeset().remove(() => true).insert(data))
                res.view.resize();

                // NOTE : 見やすいようにとりあえず 400px に固定
                res.view.width(400);
                res.view.height(400);

                res.view.runAsync();
            })
        }
    }, [spec, data, theme])
    return <div ref={container}></div>
}