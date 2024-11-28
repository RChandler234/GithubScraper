import { numberInputClasses } from "@mui/base/Unstable_NumberInput";
import { styled } from "@mui/system";
import { blue, grey } from "./colors";

const StyledInputRoot = styled("div")(
  ({ theme }) => `
    font-family: 'IBM Plex Sans', sans-serif;
    font-weight: 400;
    border-radius: 8px;
    color: ${theme.palette.mode === "dark" ? grey[300] : grey[900]};
    background: ${theme.palette.mode === "dark" ? grey[900] : "#fff"};
    border: 1px solid ${theme.palette.mode === "dark" ? grey[700] : grey[200]};
    box-shadow: 0 2px 2px ${
      theme.palette.mode === "dark" ? grey[900] : grey[50]
    };
    display: grid;
    grid-template-columns: 1fr 19px;
    grid-template-rows: 1fr 1fr;
    overflow: hidden;
    column-gap: 8px;
    padding: 4px;
  
    &.${numberInputClasses.focused} {
      border-color: ${blue[400]};
      box-shadow: 0 0 0 3px ${
        theme.palette.mode === "dark" ? blue[600] : blue[200]
      };
    }
  
    &:hover {
      border-color: ${blue[400]};
    }
  
    /* firefox */
    &:focus-visible {
      outline: 0;
    }
  `
);

export default StyledInputRoot;
