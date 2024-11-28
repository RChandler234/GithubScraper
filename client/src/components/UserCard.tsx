import { Card, CardContent, Link, Typography } from "@mui/material";
import { User } from "../utils/types";
import { datetimePipe } from "../utils/pipes";

/**
 * Card Component to Visualize User Data
 */
const UserCard = ({ user }: { user: User }) => {
  return (
    <Card sx={{ width: "100%", border: "solid 1px #E0E0E0" }}>
      <CardContent
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          gap: 1,
        }}
      >
        <Link
          variant="h6"
          target="_blank"
          rel="noreferrer"
          href={`https://github.com/${user.username}`}
          sx={{ textDecoration: "none" }}
        >
          {user.username}
        </Link>
        <Typography>{`Created at ${datetimePipe(user.createdAt)}`}</Typography>
      </CardContent>
    </Card>
  );
};

export default UserCard;
