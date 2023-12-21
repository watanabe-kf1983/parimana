import { MathJax } from 'better-react-mathjax';
import React from 'react';
import Plot from 'react-plotly.js';

// Propsの型を定義
interface PlotlyChartProps {
    chartJSON: string; // PlotlyグラフのJSON文字列
}

export const PlotlyChart: React.FC<PlotlyChartProps> = ({ chartJSON }) => {
    // JSON文字列をオブジェクトにデシリアライズ
    const graphData = JSON.parse(chartJSON);

    return (
        <MathJax>
            <Plot
                data={graphData.data}  // データポイント
                layout={graphData.layout}  // レイアウト設定
            />
        </MathJax>
    );
};

