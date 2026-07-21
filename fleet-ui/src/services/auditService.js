import apiClient from "../api/apiClient";

export const getAuditLogs =async () => {
    const response = await apiClient.get("/audit-logs",{params: {_ts: Date.now(),},});

    return response.data;
  };