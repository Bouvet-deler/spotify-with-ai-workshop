import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./styles/App.css";
import { PlaylistsPage } from "./pages/PlaylistsPage";
import { CoverGeneratorPage } from "./pages/CoverGeneratorPage";
import { Navbar } from "./components/Navbar/Navbar";

function App() {
  return (
    <div>
      <Router>
        <div className="header-container">
          <Navbar />
        </div>

        <div className="content">
          <Routes>
            <Route path="/" element={<PlaylistsPage />} />
            <Route path="/cover/:playlistId" element={<CoverGeneratorPage />} />
          </Routes>
        </div>
      </Router>
    </div>
  );
}

export default App;
