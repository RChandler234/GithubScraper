import {
  Box,
  Button,
  CircularProgress,
  FormControl,
  FormHelperText,
  Typography,
} from "@mui/material";
import CustomNumberInput from "../../components/CustomNumberInput";
import { useState } from "react";
import UserCard from "../../components/UserCard";
import { useRecentUsers } from "../../hooks/users.hooks";
import { ErrorComponent } from "../../components/ErrorComponent";

const RecentUsersPage = () => {
  const [numInputValue, setNumInputValue] = useState<number | null>(null);
  const [numUsers, setNumUsers] = useState<number>(0);
  const [formError, setFormError] = useState<string | undefined>(undefined);

  const { data: users, isLoading, isError, error } = useRecentUsers(numUsers);

  const handleInputValChange = (val: number | null) => {
    if (val && val < 0) {
      setFormError("Number of Users Must be Postive");
    } else {
      setFormError(undefined);
      setNumInputValue(val);
    }
  };

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
          <FormControl variant="standard" fullWidth>
            <CustomNumberInput
              value={numInputValue}
              setValue={handleInputValChange}
            />
            {formError && (
              <FormHelperText
                id="component-error-text"
                sx={{ color: "#B94A48" }}
              >
                {formError}
              </FormHelperText>
            )}
          </FormControl>
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
        {isError || error ? (
          <ErrorComponent errorMessage={error.message} />
        ) : isLoading || !users ? (
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
