import { styled } from "@mui/system";
import { grey } from "./colors";

/**
 * Styled Input Element for Custom Inputs
 * Taken from https://mui.com/base-ui/react-number-input/
 */
const StyledInputElement = styled("input")(
  ({ theme }) => `
    font-size: 0.875rem;
    font-family: inherit;
    font-weight: 400;
    line-height: 1.5;
    grid-column: 1/2;
    grid-row: 1/3;
    color: ${theme.palette.mode === "dark" ? grey[300] : grey[900]};
    background: inherit;
    border: none;
    border-radius: inherit;
    padding: 8px 12px;
    outline: 0;
  `
);

export default StyledInputElement;
