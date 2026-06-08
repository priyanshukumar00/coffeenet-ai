import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

const AdminDashboard = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate("/login", { replace: true });
  };

  return (
    <main>
      <section>
        <h1>Admin Dashboard</h1>
        <p>Welcome to CoffeeNet admin panel.</p>

        <div>
          <p>
            Logged in as: <strong>{user?.email}</strong>
          </p>

          <p>
            Role: <strong>{user?.role}</strong>
          </p>

          <button onClick={handleLogout}>Logout</button>
        </div>
      </section>
    </main>
  );
};

export default AdminDashboard;