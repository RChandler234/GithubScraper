import { Box, Button, CircularProgress, Typography } from "@mui/material";
import ProjectCard from "../../components/ProjectCard";
import { useState } from "react";
import { useUserProjects } from "../../hooks/users.hooks";
import CustomStringInput from "../../components/CustomTextInput";
import { Project } from "../../utils/types";

const UserProjectsPage = () => {
  const [inputValue, setInputValue] = useState<string>("");
  const [username, setUsername] = useState<string>("");

  const {
    data: projects,
    isLoading,
    isError,
    error,
  } = useUserProjects(username);

  if (isError) {
    return <div>{error.message}</div>;
  }

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
          <CustomStringInput
            value={inputValue}
            setValue={setInputValue}
            placeholder="Enter a Username..."
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
        {isLoading ? (
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
