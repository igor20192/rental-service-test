import { createContext, useContext, useEffect, useState } from "react";
import api from "../api/axios";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const refreshToken = async () => {
      try {
        await api.post("/auth/refresh/", {}, { withCredentials: true });
        await fetchUser();
      } catch (error) {
        console.error("Failed to refresh token", error);
        setUser(null);
      }
    };
  
    const interval = setInterval(refreshToken, 4 * 60 * 1000); 
    refreshToken(); 
  
    return () => clearInterval(interval);
  }, []);
  

  const fetchUser = () => {
    return api
      .get("/auth/me/")
      .then((res) => setUser(res.data))
      .catch(() => setUser(null))
      .finally(() => setLoading(false));
  };

  const login = async (email, password) => {
    await api.post("auth/login/", { email, password });
    await fetchUser(); 
  };

  const logout = async () => {
    await api.post("/auth/logout/");
    setUser(null);
  };

  useEffect(() => {
    fetchUser();
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
