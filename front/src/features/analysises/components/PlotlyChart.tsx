import { MathJax } from 'better-react-mathjax';
import React from 'react';
import Plot from 'react-plotly.js';
import { useWindowSize } from '../hooks/useWindowSize';

// Propsの型を定義
interface PlotlyChartProps {
    chartJSON: string; // PlotlyグラフのJSON文字列
}

export const PlotlyChart: React.FC<PlotlyChartProps> = ({ chartJSON }) => {
    // JSON文字列をオブジェクトにデシリアライズ
    const graphData = JSON.parse(chartJSON);

    const windowWidth = useWindowSize();

    const graphWidth = windowWidth > 600 ? windowWidth - 20 : 580
    const graphHeight = windowWidth > 600 ? graphWidth * 3 / 4 : graphWidth
    graphData.layout.width = graphWidth;
    graphData.layout.height = graphHeight;

    if ('legend' in graphData.layout && windowWidth > 600) {
        graphData.layout.legend.xanchor = "right";
        graphData.layout.legend.yanchor = "top";
        graphData.layout.legend.x = 0.99;
        graphData.layout.legend.y = 0.99;
        graphData.layout.legend.orientation = "v";
    }

    return (
        <MathJax>
            <Plot
                data={graphData.data}
                layout={graphData.layout}
            />
        </MathJax>
    );
};

