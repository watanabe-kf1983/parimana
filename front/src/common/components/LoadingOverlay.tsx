import { Box, CircularProgress } from "@mui/material";

type Props = { loading: boolean, zindex?: number };

export function LoadingOverlay(props: Props) {
    return (
        props.loading &&
        <Box
            aria-busy={true}
            sx={{
                position: "absolute",
                inset: 0,
                bgcolor: "background.paper",
                opacity: 0.8,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                zIndex: props.zindex ?? 1,
                pointerEvents: "auto", // オーバーレイがクリック吸う
            }}
        >
            <CircularProgress size="5rem"/>
        </Box>
    );
}