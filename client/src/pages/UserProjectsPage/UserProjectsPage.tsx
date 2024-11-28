import {
  Box,
  Button,
  CircularProgress,
  FormControl,
  FormHelperText,
  Typography,
} from "@mui/material";
import ProjectCard from "../../components/ProjectCard";
import { useState } from "react";
import { useUserProjects } from "../../hooks/users.hooks";
import CustomStringInput from "../../components/CustomTextInput";
import { Project } from "../../utils/types";
import { ErrorComponent } from "../../components/ErrorComponent";

const GITHUB_USERNAME_REGEX = /^[a-zA-Z0-9-]+$/;

const UserProjectsPage = () => {
  const [inputValue, setInputValue] = useState<string>("");
  const [username, setUsername] = useState<string>("");
  const [formError, setFormError] = useState<string | undefined>(undefined);

  const handleInputValChange = (val: string) => {
    if (val.length > 0 && !GITHUB_USERNAME_REGEX.test(val)) {
      setFormError("Must only contain alphanumeric characters or -");
    } else if (val.length > 39) {
      setFormError("Must be less than 40 characters");
    } else {
      setFormError(undefined);
      setInputValue(val);
    }
  };

  const {
    data: projects,
    isLoading,
    isError,
    error,
  } = useUserProjects(username);

  let displayProjects: Project[] = [];
  if (username.length > 0) {
    displayProjects = projects || [];
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
          User Projects
        </Typography>
        <Box marginY="15px" marginX="30px">
          <FormControl variant="standard" fullWidth>
            <CustomStringInput
              value={inputValue}
              setValue={handleInputValChange}
              placeholder="Enter a Username..."
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
            onClick={() => setUsername(inputValue || "")}
          >
            Fetch Projects
          </Button>
        </Box>
        {projects && (
          <Box marginY="15px" marginX="30px">
            <Typography>{`${projects.length} Projects Fetched`}</Typography>
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
        ) : isLoading ? (
          <CircularProgress />
        ) : (
          displayProjects.map((project, idx) => (
            <Box
              key={`${project.name}-${project.userid}-${idx}`}
              marginBottom={"10px"}
              width="100%"
            >
              <ProjectCard project={project} />
            </Box>
          ))
        )}
      </Box>
    </Box>
  );
};

export default UserProjectsPage;
