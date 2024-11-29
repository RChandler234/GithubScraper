import { useQuery } from "react-query";
import { User } from "../utils/types";
import { getRecentUsers } from "../apis/users.api";

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
    },
    {
      retry: 1,
    }
  );
};
