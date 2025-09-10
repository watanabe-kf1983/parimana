import { MathJax } from 'better-react-mathjax';
import React from 'react';
import Plot from 'react-plotly.js';
import { useWindowSize } from '../hooks/useWindowSize';
import { Box } from '@mui/material';

// Propsの型を定義
interface PlotlyChartProps {
    chartJSON: string; // PlotlyグラフのJSON文字列
}

export const PlotlyChart: React.FC<PlotlyChartProps> = ({ chartJSON }) => {
    // JSON文字列をオブジェクトにデシリアライズ
    const MAX_GRAPH_WIDTH = 1000;
    const FRAME_PADDING = 15;
    const graphWidth = Math.min(useWindowSize() - FRAME_PADDING * 2, MAX_GRAPH_WIDTH)
    const graphHeight = graphWidth * 3 / 4

    const graphData = JSON.parse(chartJSON);
    graphData.layout.width = graphWidth;
    graphData.layout.height = graphHeight;

    if ('legend' in graphData.layout && graphWidth > 700) {
        graphData.layout.legend.xanchor = "right";
        graphData.layout.legend.yanchor = "top";
        graphData.layout.legend.x = 0.99;
        graphData.layout.legend.y = 0.99;
        graphData.layout.legend.orientation = "v";
    }
    if ('legend' in graphData.layout) {
        graphData.layout.showlegend = graphWidth > 450;
    }
    graphData.layout.autosize = true;

    return (
        <Box my={2}>
            <MathJax>
                <Plot
                    data={graphData.data}
                    useResizeHandler={true}
                    layout={graphData.layout}
                    config={{ displayModeBar: graphWidth > 700 }}
                />
            </MathJax>
        </Box>
    );
};

