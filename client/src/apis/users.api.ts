import {
  Project,
  RequestBodyProject,
  RequestBodyUser,
  User,
} from "../utils/types";
import { apiUrls } from "../utils/urls";

/**
 * Fetch n Most Recently Added Users.
 * Transforms Response to Frontend Type.
 *
 * @param numUsers the number of recent users to return
 */
export const getRecentUsers = async (numUsers: number): Promise<User[]> => {
  const response = await fetch(apiUrls.usersMostRecent(numUsers));
  const { users } = await response.json();
  return users.map((user: RequestBodyUser) => {
    return { ...user, createdAt: new Date(user.created_at) };
  });
};

/**
 * Fetch Projects for a Given Github Username
 * Transforms Response to Frontend Type.
 *
 * @param username the Github Username whose projects are being fetched
 */
export const getUserProjects = async (username: string): Promise<Project[]> => {
  const response = await fetch(apiUrls.usersProjectsByUsername(username));
  const { projects } = await response.json();
  return projects.map((project: RequestBodyProject) => {
    return { ...project, createdAt: new Date(project.created_at) };
  });
};
