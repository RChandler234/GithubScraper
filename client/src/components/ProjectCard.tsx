import { Card, CardContent, Link, Stack, Typography } from "@mui/material";
import { Project } from "../utils/types";
import StarIcon from "@mui/icons-material/Star";
import AltRouteIcon from "@mui/icons-material/AltRoute";

/**
 * Card Component to Visualize Project Metadata
 */
const ProjectCard = ({ project }: { project: Project }) => {
  return (
    <Card sx={{ width: "100%", border: "solid 1px #E0E0E0" }}>
      <CardContent>
        <Link
          variant="h6"
          target="_blank"
          rel="noreferrer"
          href={`https://github.com/${project.username}/${project.name}`}
          sx={{ textDecoration: "none" }}
        >
          {project.name}
        </Link>
        <Typography>{project.description}</Typography>
        <Stack alignItems="center" direction="row" gap={2}>
          <Stack alignItems="center" direction="row" gap={1}>
            <StarIcon fontSize="small" />
            <Typography>{`${project.stars} stars`}</Typography>
          </Stack>
          <Stack alignItems="center" direction="row" gap={1}>
            <AltRouteIcon fontSize="small" />
            <Typography>{`${project.forks} forks`}</Typography>
          </Stack>
        </Stack>
      </CardContent>
    </Card>
  );
};

export default ProjectCard;
