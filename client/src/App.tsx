import "./App.css";
import NavBar from "./components/layout/NavBar";
import QueryClientContext from "./contexts/query.context";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom";
import UserProjectsPage from "./pages/UserProjectsPage/UserProjectsPage";
import StarredProjectsPage from "./pages/StarredProjectsPage/StarredProjectsPage";
import RecentUsersPage from "./pages/RecentUsersPage/RecentUsersPage";
import ThemeContext from "./contexts/theme.context";

function App() {
  return (
    <QueryClientContext>
      <ThemeContext>
        <Router>
          <NavBar />
          <Routes>
            <Route
              path="/"
              element={<Navigate to="/user-projects" replace />}
            />
            <Route path="/most-recent-users" element={<RecentUsersPage />} />
            <Route
              path="/most-starred-projects"
              element={<StarredProjectsPage />}
            />
            <Route path="/user-projects" element={<UserProjectsPage />} />
          </Routes>
        </Router>
      </ThemeContext>
    </QueryClientContext>
  );
}

export default App;
