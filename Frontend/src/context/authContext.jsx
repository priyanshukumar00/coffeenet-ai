import { createContext, useContext, useEffect, useState } from "react";
import { loginUser, getMe } from "../api/authApi";
import {
  saveToken,
  saveUser,
  getToken,
  getUser,
  clearAuthStorage,
} from "../utils/token";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(getUser());
  const [token, setToken] = useState(getToken());
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const verifyUserSession = async () => {
      try {
        const existingToken = getToken();

        if (!existingToken) {
          setLoading(false);
          return;
        }

        const currentUser = await getMe();

        setUser(currentUser);
        saveUser(currentUser);
      } catch (error) {
        console.error("Session verification failed:", error.message);
        clearAuthStorage();
        setUser(null);
        setToken(null);
      } finally {
        setLoading(false);
      }
    };

    verifyUserSession();
  }, []);

  const login = async ({ username, password }) => {
    try {
      const data = await loginUser({ username, password });

      if (!data?.access_token) {
        throw new Error("Login failed. Token not received from server.");
      }

      saveToken(data.access_token);
      setToken(data.access_token);

      const currentUser = await getMe();

      saveUser(currentUser);
      setUser(currentUser);

      return currentUser;
    } catch (error) {
      clearAuthStorage();
      setUser(null);
      setToken(null);
      throw new Error(error.message || "Login failed.");
    }
  };

  const logout = () => {
    clearAuthStorage();
    setUser(null);
    setToken(null);
  };

  const value = {
    user,
    token,
    loading,
    isAuthenticated: Boolean(token && user),
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider.");
  }

  return context;
};