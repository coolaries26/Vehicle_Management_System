import apiClient from "../api/apiClient";

export const getComplaints = async () => {
  const response = await apiClient.get("/complaints");
  return response.data;
};

export const createComplaint = async (payload) => {
  const response = await apiClient.post("/complaints", payload);
  return response.data;
};

export const updateComplaint = async (complaintId, payload) => {
  const response = await apiClient.put(`/complaints/${complaintId}`, payload);
  return response.data;
};

export const deactivateComplaint = async (complaintId) => {
  const response = await apiClient.put(`/complaints/${complaintId}`, { active_flag: false });
  return response.data;
};