import { PropsWithChildren } from "react";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";

const theme = createTheme({
  palette: {
    background: {
      default: "#010409",
      paper: "#0A0A0A",
    },
    text: {
      primary: "#E0E0E0",
      secondary: "##b0b0b0",
    },
  },
  typography: {
    button: {
      textTransform: "none",
    },
  },
});

/**
 * Context to Provide MUI Theme to the whole app
 */
const ThemeContext = (props: PropsWithChildren) => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {props.children}
    </ThemeProvider>
  );
};

export default ThemeContext;
