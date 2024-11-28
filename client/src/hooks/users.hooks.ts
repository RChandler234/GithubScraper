import { useQuery } from "react-query";
import { Project, User } from "../utils/types";
import { getRecentUsers, getUserProjects } from "../apis/users.api";

/**
 * Custom React Hook to supply the n most recently added users
 *
 * @param numUsers the number of users to return
 */
export const useRecentUsers = (numUsers: number) => {
  return useQuery<User[], Error>(
    ["users", "most-recent", numUsers],
    async () => {
      const data = await getRecentUsers(numUsers);
      return data;
    }
  );
};

/**
 * Custom React Hook to fetch a users projects
 *
 * @param username the username of the user whose projects are being fetched
 */
export const useUserProjects = (username: string) => {
  return useQuery<Project[], Error>(
    ["projects", username],
    async () => {
      const data = await getUserProjects(username);
      return data;
    },
    {
      // The query will not execute unless a non-empty username is entered
      enabled: username.length > 0,
    }
  );
};
