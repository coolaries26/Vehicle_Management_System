import apiClient from "../api/apiClient";

export const getChecklists = async () => {
  const response = await apiClient.get("/checklists",{params: {_ts: Date.now(),},});

  return response.data;
};

export const createChecklist = async (payload) => {
  const response =await apiClient.post("/checklists",payload);

  return response.data;
};

export const updateChecklist = async (checklistId,payload) => {
  const response =await apiClient.put(`/checklists/${checklistId}`,payload);

  return response.data;
};

export const deactivateChecklist =async (checklistId) => {
    const response =  await apiClient.put(`/checklists/${checklistId}`,{active_flag: false,});

    return response.data;};