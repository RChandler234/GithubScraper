/**
 * File for all the URLs used to query the API.
 */

const API_URL: string =
  import.meta.env.VITE_REACT_APP_BACKEND_URL || "http://localhost:5000";

/**************** Users Endpoints ****************/
const users = () => `${API_URL}/users`;
const usersProjectsByUsername = (username: string) =>
  `${users()}/projects/${username}`;
const usersMostRecent = (maxNumUsers: number) =>
  `${users()}/most-recent/${maxNumUsers}`;

/**************** Projects Endpoints ****************/
const projects = () => `${API_URL}/projects`;
const projectsMostStarred = (maxNumProjects: number) =>
  `${projects()}/most-starred/${maxNumProjects}`;

export const apiUrls = {
  users,
  usersProjectsByUsername,
  usersMostRecent,

  projects,
  projectsMostStarred,
};
