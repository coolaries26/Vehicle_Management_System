import apiClient from "../api/apiClient";

export const getVehicles = async () => {
  const response = await apiClient.get("/vehicles", {
    params: {
      _ts: Date.now(),
    },
  });

  return response.data;
};

export const getVehicleById = async (vehicleId) => {
  const response = await apiClient.get(`/vehicles/${vehicleId}`);

  return response.data;
};

export const createVehicle = async (payload) => {
  const response = await apiClient.post("/vehicles", payload);

  return response.data;
};

export const updateVehicle = async (vehicleId, payload) => {
  const response = await apiClient.put(`/vehicles/${vehicleId}`, payload);

  return response.data;
};

export const deleteVehicle = async (vehicleId) => {
  const response = await apiClient.put(`/vehicles/${vehicleId}`, {"active_flag": false});

  return response.data;
};

