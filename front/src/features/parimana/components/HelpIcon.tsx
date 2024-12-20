import { IconButton, Tooltip } from "@mui/material";
import HelpOutlineIcon from "@mui/icons-material/HelpOutline";

export function HelpIcon() {
    const openHelp = () => {
        window.open("/about", "_blank");
    };

    return (
        <Tooltip title={<span style={{ fontSize: "0.9rem" }}>parimanaについて</span>}>
            <IconButton onClick={openHelp} sx={{ m: 1 }}>
                <HelpOutlineIcon />
            </IconButton>
        </Tooltip >
    );
};
