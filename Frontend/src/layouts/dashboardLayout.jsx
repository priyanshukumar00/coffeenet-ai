import { Outlet, NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const DashboardLayout = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login", { replace: true });
  };

  return (
    <div className="dashboard-layout">
      <aside className="dashboard-sidebar">
        <h2>CoffeeNet</h2>

        <nav>
          <NavLink to="/admin/dashboard">Dashboard</NavLink>
          <NavLink to="/admin/menu">Menu</NavLink>
          <NavLink to="/admin/inventory">Inventory</NavLink>
          <NavLink to="/admin/recipes">Recipes</NavLink>
          <NavLink to="/admin/orders">Orders</NavLink>
          <NavLink to="/admin/users">Users</NavLink>
        </nav>
      </aside>

      <div className="dashboard-main">
        <header className="dashboard-header">
          <div>
            <h3>{user?.role} Panel</h3>
            <p>{user?.email}</p>
          </div>

          <button onClick={handleLogout}>Logout</button>
        </header>

        <section className="dashboard-content">
          <Outlet />
        </section>
      </div>
    </div>
  );
};

export default DashboardLayout;