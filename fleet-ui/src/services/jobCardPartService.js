import apiClient from "../api/apiClient";
export const getJobCardParts =async () => {
const response =await apiClient.get("/jobcard-parts",{params: {_ts: Date.now(),},});

return response.data;
};
export const createJobCardPart = async (payload) => {
const response = await apiClient.post("/jobcard-parts",payload);

return response.data;
};
export const updateJobCardPart = async (id,payload) => {
const response =await apiClient.put(`/jobcard-parts/${id}`,payload);

return response.data;
};
export const deactivateJobCardPart = async (id) => {
const response =
  await apiClient.put(`/jobcard-parts/${id}`,{active_flag: false,});

return response.data;
};