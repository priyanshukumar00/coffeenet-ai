import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

const Login = () => {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const getDashboardPath = (role) => {
    const normalizedRole = role?.toLowerCase();

    switch (normalizedRole) {
      case "admin":
        return "/admin/dashboard";
      case "manager":
        return "/manager/dashboard";
      case "cashier":
        return "/cashier/dashboard";
      case "kitchen":
        return "/kitchen/dashboard";
      default:
        return "/unauthorized";
    }
  };

  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));

    setError("");
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!formData.username.trim() || !formData.password.trim()) {
      setError("Please enter both username and password.");
      return;
    }

    try {
      setLoading(true);
      setError("");

      const user = await login({
        username: formData.username.trim(),
        password: formData.password,
      });

      const redirectPath = getDashboardPath(user?.role);
      navigate(redirectPath, { replace: true });
    } catch (error) {
      setError(error.message || "login failed! Verify your credentials and try again");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main>
      <section>
        <h1>CoffeeNet Login</h1>
        <p>Login to continue to your dashboard.</p>

        <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor="username">Username / Email</label>
            <input
              id="username"
              name="username"
              type="text"
              value={formData.username}
              onChange={handleChange}
              placeholder="Enter your username"
              autoComplete="username"
            />
          </div>

          <div>
            <label htmlFor="password">Password</label>
            <input
              id="password"
              name="password"
              type="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Enter your password"
              autoComplete="current-password"
            />
          </div>

          {error && <p style={{ color: "red" }}>{error}</p>}

          <button type="submit" disabled={loading}>
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>
      </section>
    </main>
  );
};

export default Login;