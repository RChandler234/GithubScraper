import { Box, Button, CircularProgress, Typography } from "@mui/material";
import { useMostStarredProjects } from "../../hooks/projects.hooks";
import ProjectCard from "../../components/ProjectCard";
import CustomNumberInput from "../../components/CustomNumberInput";
import { useState } from "react";

const StarredProjectsPage = () => {
  const [numInputValue, setNumInputValue] = useState<number | null>(null);
  const [numProjects, setNumProjects] = useState<number>(0);

  const {
    data: projects,
    isLoading,
    isError,
    error,
  } = useMostStarredProjects(numProjects);

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
          Most Starred Projects
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
            onClick={() => setNumProjects(numInputValue || 0)}
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
        {isLoading || !projects ? (
          <CircularProgress />
        ) : (
          projects.map((project, idx) => (
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

export default StarredProjectsPage;
