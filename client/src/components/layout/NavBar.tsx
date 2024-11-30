import {
  AppBar,
  Box,
  Button,
  Container,
  Icon,
  IconButton,
  ListItemIcon,
  ListItemText,
  Menu,
  MenuItem,
  Toolbar,
  Typography,
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import React from "react";
import CloudDownloadIcon from "@mui/icons-material/CloudDownload";
import { useNavigate } from "react-router-dom";

const NAV_BUTTONS = [
  {
    title: "User Projects",
    url: "/user-projects",
    icon: "folder",
  },
  {
    title: "Starred Projects",
    url: "/most-starred-projects",
    icon: "star",
  },
  {
    title: "Recent Users",
    url: "/most-recent-users",
    icon: "person",
  },
];

/**
 * Custom Responsive NavBar (https://mui.com/material-ui/react-app-bar/#app-bar-with-responsive-menu)
 */
const NavBar = () => {
  const navigate = useNavigate();
  const [anchorElNav, setAnchorElNav] = React.useState<null | HTMLElement>(
    null
  );

  const handleOpenNavMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorElNav(event.currentTarget);
  };

  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };

  const handleClickMenuItem = (url: string) => {
    handleCloseNavMenu();
    navigate(url);
  };

  const handleClickNavBarButton = (url: string) => {
    handleCloseNavMenu();
    navigate(url);
  };

  return (
    <AppBar
      position="static"
      sx={{
        backgroundColor: "#151b23f2",
        color: "#ffffffb3",
      }}
    >
      <Container maxWidth={false}>
        <Toolbar
          disableGutters
          sx={{ display: "flex", justifyContent: "space-between" }}
        >
          <Box
            alignItems={"center"}
            gap={1}
            flexGrow={5}
            sx={{ display: { xs: "none", md: "flex" } }}
          >
            <CloudDownloadIcon
              sx={{ display: { xs: "none", md: "flex" }, mr: 1 }}
            />
            <Typography
              variant="h6"
              noWrap
              sx={{
                mr: 2,
                display: { xs: "none", md: "flex" },
                fontWeight: 700,
                color: "inherit",
                textDecoration: "none",
              }}
            >
              Github Project Scraper
            </Typography>
          </Box>

          <Box sx={{ flexGrow: 1, display: { xs: "flex", md: "none" } }}>
            <IconButton
              size="large"
              aria-label="account of current user"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              onClick={handleOpenNavMenu}
              color="inherit"
            >
              <MenuIcon />
            </IconButton>
            <Menu
              id="menu-appbar"
              anchorEl={anchorElNav}
              anchorOrigin={{
                vertical: "bottom",
                horizontal: "left",
              }}
              keepMounted
              transformOrigin={{
                vertical: "top",
                horizontal: "left",
              }}
              open={Boolean(anchorElNav)}
              onClose={handleCloseNavMenu}
              sx={{ display: { xs: "block", md: "none" } }}
            >
              {NAV_BUTTONS.map((button) => (
                <MenuItem
                  key={button.title}
                  onClick={() => handleClickMenuItem(button.url)}
                >
                  <ListItemIcon>
                    <Icon sx={{ color: "#ffffffb3" }}>{button.icon}</Icon>
                  </ListItemIcon>
                  <ListItemText sx={{ textAlign: "center" }}>
                    {button.title}
                  </ListItemText>
                </MenuItem>
              ))}
            </Menu>
          </Box>
          <CloudDownloadIcon
            sx={{ display: { xs: "flex", md: "none" }, mr: 1 }}
          />
          <Typography
            variant="h5"
            noWrap
            sx={{
              mr: 2,
              display: { xs: "flex", md: "none" },
              flexGrow: 1,
              fontWeight: 700,
              color: "inherit",
              textDecoration: "none",
            }}
          >
            Github Project Scraper
          </Typography>
          <Box
            sx={{
              flexGrow: 1,
              display: { xs: "none", md: "flex" },
              justifyContent: "space-evenly",
            }}
          >
            {NAV_BUTTONS.map((button) => (
              <Button
                key={button.title}
                onClick={() => handleClickNavBarButton(button.url)}
                startIcon={<Icon>{button.icon}</Icon>}
                sx={{
                  my: 1,
                  color: "inherit",
                  fontSize: "16px",
                  lineHeight: 1.5,
                }}
              >
                {button.title}
              </Button>
            ))}
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default NavBar;
