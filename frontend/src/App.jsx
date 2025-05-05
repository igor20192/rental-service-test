import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ApartmentList from "./components/ApartmentList";
import ApartmentDetail from "./components/ApartmentDetail";
import LoginPage from "./components/LoginPage";
import Navbar from "./components/Navbar";
import ProtectedRoute from "./components/ProtectedRoute";
import ApartmentCreateForm from "./components/ApartmentCreateForm";
import ApartmentEditForm from "./components/ApartmentEditForm";




export default function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/" element={<ApartmentList />} />
        <Route path="/apartments/:slug" element={<ApartmentDetail />} />
        <Route path="/apartments/create" element={<ProtectedRoute><ApartmentCreateForm /></ProtectedRoute>} />
        <Route path="/apartments/:slug/edit" element={<ProtectedRoute><ApartmentEditForm /></ProtectedRoute>} />
      </Routes>
    </Router>
  );
}

