import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Chat from "./pages/Chat";

export default function App() {
  return (
    <Router>
      <Navbar />
      <div style={{ padding: "10px" }}>
        <Link to="/">Home</Link> | <Link to="/chat">Chat</Link>
      </div>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/chat" element={<Chat />} />
      </Routes>
    </Router>
  );
}
