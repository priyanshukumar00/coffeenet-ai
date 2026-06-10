import axiosInstance from "./axiosInstance";

export const getMenuItems = async () => {
  try {
    const response = await axiosInstance.get("/menu");

    return response.data?.menu || [];
  } catch (error) {
    const message =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      "Unable to fetch menu items.";

    throw new Error(message);
  }
};

export const createMenuItem = async (menuData) => {
  try {
    const response = await axiosInstance.post("/menu", menuData);
    return response.data;
  } catch (error) {
    const message =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      "Unable to create menu item.";

    throw new Error(message);
  }
};

export const updateMenuItem = async (itemId, menuData) => {
  try {
    const response = await axiosInstance.put(`/menu/${itemId}`, menuData);
    return response.data;
  } catch (error) {
    const message =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      "Unable to update menu item.";

    throw new Error(message);
  }
};

export const patchMenuItem = async (itemId, menuData) => {
  try {
    const response = await axiosInstance.patch(`/menu/${itemId}`, menuData);
    return response.data;
  } catch (error) {
    const message =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      "Unable to update menu item.";

    throw new Error(message);
  }
};

export const deleteMenuItems = async (ids) => {
  try {
    const response = await axiosInstance.delete("/menu", {
      data: ids,
    });

    return response.data;
  } catch (error) {
    const message =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      "Unable to delete menu item.";

    throw new Error(message);
  }
};