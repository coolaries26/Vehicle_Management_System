import apiClient from "../api/apiClient";

export const getEmployees = async () => {
  const response = await apiClient.get("/employees", {
    params: {
      _ts: Date.now(),
    },
  });

  return response.data;
};

export const getEmployeeById = async (employeeId) => {
  const response = await apiClient.get(`/employees/${employeeId}`);

  return response.data;
};

export const createEmployee = async (payload) => {
  const response = await apiClient.post("/employees", payload);

  return response.data;
};

export const updateEmployee = async (employeeId, payload) => {
  const response = await apiClient.put(`/employees/${employeeId}`, payload);

  return response.data;
};

export const deleteEmployee = async (employeeId) => {
  const response = await apiClient.put(`/employees/${employeeId}`, {"active_flag": false});

  return response.data;
};