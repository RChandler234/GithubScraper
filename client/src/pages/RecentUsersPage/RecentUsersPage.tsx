import { Box, Button, CircularProgress, Typography } from "@mui/material";
import CustomNumberInput from "../../components/CustomNumberInput";
import { useState } from "react";
import UserCard from "../../components/UserCard";
import { useRecentUsers } from "../../hooks/users.hooks";

const RecentUsersPage = () => {
  const [numInputValue, setNumInputValue] = useState<number | null>(null);
  const [numUsers, setNumUsers] = useState<number>(0);

  const { data: users, isLoading, isError, error } = useRecentUsers(numUsers);

  if (isError) {
    return <div>{error.message}</div>;
  }

  return (
    <Box
      display="flex"
      sx={{ flexDirection: { xs: "column", md: "row" } }}
      height="85vh"
      width={"100%"}
    >
      <Box
        sx={{
          overflow: { xs: undefined, md: "hidden" },
          maxWidth: { xs: "100%", md: "40%" },
          minWidth: { xs: "100%", md: "40%" },
        }}
      >
        <Typography variant="h4" noWrap margin="30px" textAlign={"center"}>
          Most Recent Users
        </Typography>
        <Box marginY="15px" marginX="30px">
          <CustomNumberInput
            value={numInputValue}
            setValue={setNumInputValue}
          />
        </Box>
        <Box marginX="30px">
          <Button
            variant="contained"
            fullWidth
            sx={{
              backgroundColor: "#010409",
              border: "solid 1px #ffffffb3",
            }}
            onClick={() => setNumUsers(numInputValue || 0)}
          >
            Fetch Users
          </Button>
        </Box>
        {users && (
          <Box marginY="15px" marginX="30px">
            <Typography>{`${users.length} Users Fetched`}</Typography>
          </Box>
        )}
      </Box>
      <Box
        flexGrow={1}
        sx={{
          overflowY: "auto",
          padding: "20px",
        }}
      >
        {isLoading || !users ? (
          <CircularProgress />
        ) : (
          users.map((user, idx) => (
            <Box
              key={`${user.username}-${idx}`}
              marginBottom={"10px"}
              width="100%"
            >
              <UserCard user={user} />
            </Box>
          ))
        )}
      </Box>
    </Box>
  );
};

export default RecentUsersPage;
