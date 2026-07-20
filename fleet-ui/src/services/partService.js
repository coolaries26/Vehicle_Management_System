import apiClient from "../api/apiClient";

export const getParts = async () => {
  const response = await apiClient.get("/parts",{params: {_ts: Date.now(),},});

  return response.data;
};

export const createPart = async (payload) => {
  const response =await apiClient.post("/parts",payload);

  return response.data;
};

export const updatePart = async (partId,payload) => {
  const response =await apiClient.put(`/parts/${partId}`,payload);

  return response.data;
};

export const deactivatePart = async (partId) => {
  const response =await apiClient.put(`/parts/${partId}`,{active_flag: false,});

  return response.data;
};