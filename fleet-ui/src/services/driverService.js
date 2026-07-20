import apiClient from "../api/apiClient";

export const getDrivers = async () => {
  const response = await apiClient.get("/drivers");
  return response.data;
};

export const createDriver = async (payload) => {
  const response = await apiClient.post("/drivers", payload);
  return response.data;
};

export const updateDriver = async (driverId, payload) => {
  const response = await apiClient.put(`/drivers/${driverId}`, payload);
  return response.data;
};

export const deactivateDriver = async (driverId) => {
  const response = await apiClient.put(`/drivers/${driverId}`, {"active_flag": false});
  return response.data;
};