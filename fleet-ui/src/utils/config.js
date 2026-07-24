import apiClient from "../api/apiClient";

{/*
  export const API_BASE_URL =
  `http://${window.location.hostname}:8000`;
*/}
  export const API_BASE_URL =
  apiClient.defaults.baseURL;