import axios from "axios";

const API_URL = "http://localhost:8000";

export const getEmployees = async () => {
  const res = await axios.get(`${API_URL}/employees/`);
  return res.data;
};

export const addEmployee = async (employeeData) => {
  const res = await axios.post(`${API_URL}/employees/`, employeeData);
  return res.data;
};

export const updateEmployee = async (id, employeeData) => {
  const res = await axios.put(`${API_URL}/employees/${id}`, employeeData);
  return res.data;
};

export const deleteEmployee = async (id) => {
  const res = await axios.delete(`${API_URL}/employees/${id}`);
  return res.data;
};
