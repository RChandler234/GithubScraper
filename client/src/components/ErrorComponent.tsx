import { Box } from "@mui/material";

export const ErrorComponent = ({ errorMessage }: { errorMessage: string }) => {
  return (
    <Box
      display="flex"
      flexDirection="column"
      width={"100%"}
      alignContent={"center"}
      alignItems={"center"}
    >
      <h3>Oops! Something went wrong</h3>
      <p>{errorMessage}</p>
    </Box>
  );
};
