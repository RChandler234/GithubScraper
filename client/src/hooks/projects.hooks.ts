import { useQuery } from "react-query";
import { Project } from "../utils/types";
import { getMostStarredProjects } from "../apis/projects.api";

/**
 * Custom React Hook to supply the n most starred projects
 *
 * @param numProjects the number of most starred projects to return
 */
export const useMostStarredProjects = (numProjects: number) => {
  return useQuery<Project[], Error>(
    ["projects", "most-starred", numProjects],
    async () => {
      const data = await getMostStarredProjects(numProjects);
      return data;
    },
    {
      retry: 1,
    }
  );
};
