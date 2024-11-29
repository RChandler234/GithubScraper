import { sendAPIRequest } from "../utils/api-request";
import { RequestBodyUser, User } from "../utils/types";
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
