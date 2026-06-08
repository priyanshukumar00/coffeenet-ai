import axiosInstance from "./axiosInstance";

export const loginUser = async ({ username, password }) => {
  try {
    const formData = new URLSearchParams();

    formData.append("username", username);
    formData.append("password", password);

    const response = await axiosInstance.post("/login", formData, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    });

    if (!response.data?.access_token) {
      throw new Error(response.data?.message || "Invalid email or password.");
    }

    return response.data;
  } catch (error) {
    const message =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      "Login failed. Please check your credentials.";

    throw new Error(message);
  }
};

export const getMe = async () => {
  try {
    const response = await axiosInstance.get("/me");

    if (!response.data?.data) {
      throw new Error("User details not found.");
    }

    return response.data.data;
  } catch (error) {
    const message =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      "Unable to fetch current user details.";

    throw new Error(message);
  }
};