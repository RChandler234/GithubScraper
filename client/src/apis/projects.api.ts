import { Project, RequestBodyProject } from "../utils/types";
import { apiUrls } from "../utils/urls";

/**
 * Fetch n Most Starred Projects.
 * Transforms Response to Frontend Type.
 *
 * @param numProjects the number of most starred projects to return
 */
export const getMostStarredProjects = async (
  numProjects: number
): Promise<Project[]> => {
  const response = await fetch(apiUrls.projectsMostStarred(numProjects));
  const { projects } = await response.json();
  return projects.map((project: RequestBodyProject) => {
    return { ...project, createdAt: new Date(project.created_at) };
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
