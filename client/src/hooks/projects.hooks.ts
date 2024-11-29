import { useQuery } from "react-query";
import { Project } from "../utils/types";
import {
  getMostStarredProjects,
  getProjectsByUsername,
} from "../apis/projects.api";

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

/**
 * Custom React Hook to fetch a users projects
 *
 * @param username the username of the user whose projects are being fetched
 */
export const useProjectsByUsername = (username: string) => {
  return useQuery<Project[], Error>(
    ["projects", username],
    async () => {
      const data = await getProjectsByUsername(username);
      return data;
    },
    {
      // The query will not execute unless a non-empty username is entered
      enabled: username.length > 0,
    }
  );
};
