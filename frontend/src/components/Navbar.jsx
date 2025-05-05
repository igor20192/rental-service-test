import { Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

const Navbar = () => {
  const { user, logout, loading } = useAuth();

  const handleLogout = async () => {
    await logout();
    window.location.href = "/login";
  };

  return (
    <nav className="p-4 bg-gray-100 flex justify-between items-center">
      <Link to="/" className="text-xl font-bold text-blue-600">Квартиры</Link>
      {!loading && (
        <div className="flex gap-4">
          {user ? (
            <>
              <span>Привет, {user.first_name || user.email}</span>
              <button onClick={handleLogout} className="text-red-600 hover:underline">
                Выйти
              </button>
            </>
          ) : (
            <Link to="/login" className="text-blue-600 hover:underline">
              Войти
            </Link>
          )}
        </div>
      )}
    </nav>
  );
};

export default Navbar;
