import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const uploadPDFs = (files) => {
  const formData = new FormData();
  files.forEach((file) => formData.append("files", file));
  return API.post("/upload-pdf/", formData);
};

export const sendMessage = (query) => {
  return API.post("/chat/", null, { params: { query } });
};

export default API;
