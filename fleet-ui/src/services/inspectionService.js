import apiClient from "../api/apiClient";

export const getInspections =  async () => {
    const response = await apiClient.get("/inspections",{params: {_ts: Date.now(),},});

    return response.data;
  };

export const createInspection = async (payload) => {
    const response = await apiClient.post("/inspections",payload);

    return response.data;
  };

export const updateInspection = async (inspectionId,payload) => {
    const response = await apiClient.put(`/inspections/${inspectionId}`,payload);

    return response.data;
  };

export const deactivateInspection = async (inspectionId) => {
    const response = await apiClient.put(`/inspections/${inspectionId}`,{active_flag: false,});

    return response.data;
  };