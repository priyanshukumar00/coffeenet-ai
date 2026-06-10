import { Outlet, NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const DashboardLayout = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const role = user?.role?.toLowerCase();

  const sidebarLinks = {
    admin: [
      { label: "Dashboard", path: "/admin/dashboard" },
      { label: "Menu", path: "/admin/menu" },
      { label: "Inventory", path: "/admin/inventory" },
      { label: "Recipes", path: "/admin/recipes" },
      { label: "Orders", path: "/admin/orders" },
      { label: "Users", path: "/admin/users" },
    ],
    manager: [
      { label: "Dashboard", path: "/manager/dashboard" },
      { label: "Inventory", path: "/manager/inventory" },
      { label: "Recipes", path: "/manager/recipes" },
      { label: "Orders", path: "/manager/orders" },
    ],
    cashier: [
      { label: "Dashboard", path: "/cashier/dashboard" },
      { label: "Create Order", path: "/cashier/create-order" },
      { label: "Orders", path: "/cashier/orders" },
      { label: "Menu", path: "/cashier/menu" },
    ],
    kitchen: [
      { label: "Dashboard", path: "/kitchen/dashboard" },
      { label: "Kitchen Orders", path: "/kitchen/orders" },
    ],
  };

  const links = sidebarLinks[role] || [];

  const handleLogout = () => {
    logout();
    navigate("/login", { replace: true });
  };

  return (
    <div className="dashboard-layout">
      <aside className="dashboard-sidebar">
        <h2>CoffeeNet</h2>

        <nav>
          {links.map((link) => (
            <NavLink key={link.path} to={link.path}>
              {link.label}
            </NavLink>
          ))}
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