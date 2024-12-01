import {
  Box,
  Button,
  CircularProgress,
  FormControl,
  FormHelperText,
  Typography,
} from "@mui/material";
import { useMostStarredProjects } from "../../hooks/projects.hooks";
import ProjectCard from "../../components/ProjectCard";
import CustomNumberInput from "../../components/CustomNumberInput";
import { useState } from "react";
import { ErrorComponent } from "../../components/ErrorComponent";

/**
 * Main Starred Projects Page Component
 */
const StarredProjectsPage = () => {
  const [numInputValue, setNumInputValue] = useState<number | null>(null);
  const [numProjects, setNumProjects] = useState<number>(0);
  const [formError, setFormError] = useState<string | undefined>(undefined);

  const handleInputValChange = (val: number | null) => {
    if (val && val < 0) {
      setFormError("Number of Users Must be Postive");
    } else {
      setFormError(undefined);
    }
    setNumInputValue(val);
  };

  const handleButtonClick = () => {
    if (!formError) {
      setNumProjects(numInputValue || 0);
    }
  };

  const {
    data: projects,
    isLoading,
    isError,
    error,
  } = useMostStarredProjects(numProjects);

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
            onClick={handleButtonClick}
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
        ) : isLoading || !projects ? (
          <CircularProgress />
        ) : (
          projects.map((project, idx) => (
            <Box
              key={`${project.name}-${project.userId}-${idx}`}
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
