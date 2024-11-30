import { sendAPIRequest } from "../utils/api-request";
import { Project, APIResponseProject } from "../utils/types";
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
  const data = await sendAPIRequest(apiUrls.projectsMostStarred(numProjects));
  return data.projects.map((project: APIResponseProject) => {
    return { ...project, createdAt: new Date(project.created_at) };
  });
};

/**
 * Fetch Projects for a Given Github Username
 * Transforms Response to Frontend Type.
 *
 * @param username the Github Username whose projects are being fetched
 */
export const getProjectsByUsername = async (
  username: string
): Promise<Project[]> => {
  const data = await sendAPIRequest(apiUrls.projectsByUsername(username));
  return data.projects.map((project: APIResponseProject) => {
    return {
      ...project,
      userId: project.user_id,
      createdAt: new Date(project.created_at),
    };
  });
};
