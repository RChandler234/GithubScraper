import { sendAPIRequest } from "../utils/api-request";
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
  const data = await sendAPIRequest(apiUrls.usersMostRecent(numUsers));
  return data.users.map((user: RequestBodyUser) => {
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
  const data = await sendAPIRequest(apiUrls.usersProjectsByUsername(username));
  return data.projects.map((project: RequestBodyProject) => {
    return { ...project, createdAt: new Date(project.created_at) };
  });
};
