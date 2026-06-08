import { Routes, Route, Navigate } from "react-router-dom";
import AdminDashboard from "../pages/admin/AdminDashboard";
import DashboardLayout from "../layouts/DashboardLayout";

import ProtectedRoute from "../auth/ProtectedRoute";
import RoleRoute from "../auth/RoleRoute";

import Login from "../pages/auth/Login";

const AppRoutes = () => {
  return (
    <Routes>
      {/* Public Routes */}
      <Route path="/login" element={<Login />} />

      {/* Protected Routes */}
      <Route element={<ProtectedRoute />}>
        {/* Admin Routes */}
        <Route element={<RoleRoute allowedRoles={["Admin"]} />}>
          <Route element={<DashboardLayout />}>
            <Route path="/admin/dashboard" element={<AdminDashboard />} />
        </Route>
        </Route>

        {/* Manager Routes */}
        <Route element={<RoleRoute allowedRoles={["Admin", "Manager"]} />}>
          <Route path="/manager/dashboard" element={<h1>Manager Dashboard</h1>} />
        </Route>

        {/* Cashier Routes */}
        <Route element={<RoleRoute allowedRoles={["Admin", "Cashier"]} />}>
          <Route path="/cashier/dashboard" element={<h1>Cashier Dashboard</h1>} />
        </Route>

        {/* Kitchen Routes */}
        <Route element={<RoleRoute allowedRoles={["Admin", "Kitchen"]} />}>
          <Route path="/kitchen/dashboard" element={<h1>Kitchen Dashboard</h1>} />
        </Route>
      </Route>

      {/* Unauthorized Page */}
      <Route
        path="/unauthorized"
        element={<h1>You are not allowed to access this page.</h1>}
      />

      {/* Default Route */}
      <Route path="/" element={<Navigate to="/login" replace />} />

      {/* 404 Route */}
      <Route path="*" element={<h1>404 - Page Not Found</h1>} />
    </Routes>
  );
};

export default AppRoutes;