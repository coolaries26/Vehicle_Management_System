import apiClient from "../api/apiClient";

export const getPartRequisitionDetails =
  async () => {

    const response =
      await apiClient.get(
        "/requisition-details",
        {
          params: {
            _ts: Date.now(),
          },
        }
      );

    return response.data;
  };

export const createPartRequisitionDetail =
  async (payload) => {

    const response =
      await apiClient.post(
        "/requisition-details",
        payload
      );

    return response.data;
  };

export const updatePartRequisitionDetail =
  async (
    detailId,
    payload
  ) => {

    const response =
      await apiClient.put(
        `/requisition-details/${detailId}`,
        payload
      );

    return response.data;
  };

export const deactivatePartRequisitionDetail =
  async (
    detailId
  ) => {

    const response =
      await apiClient.delete(
        `/requisition-details/${detailId}`
      );

    return response.data;
  };