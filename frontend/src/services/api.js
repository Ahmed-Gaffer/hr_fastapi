import axios from "axios";

const API_BASE = process.env.REACT_APP_API_URL || "http://192.168.10.92:8000/api";

const getTenantId = () =>
  localStorage.getItem("tenantId") || process.env.REACT_APP_TENANT_ID || "1";

const axiosInstance = axios.create({ baseURL: API_BASE });

axiosInstance.interceptors.request.use((config) => {
  config.headers["X-Tenant-ID"] = getTenantId();
  return config;
});

const getErrorMessage = (err, fallback) =>
  err.response?.data?.detail || err.response?.data?.error || err.message || fallback;

export async function fetchEmployees() {
  const res = await axiosInstance.get("/employees/");
  return res.data.map((e) => ({
    ...e,
    role: e.job_title || "-",
    site: e.site_name || "-",
    costCenter: e.cost_center_name || "-",
  }));
}

export async function fetchEmployee(id) {
  const res = await axiosInstance.get(`/employees/${id}`);
  return res.data;
}

export async function fetchAttendances() {
  const res = await axiosInstance.get("/attendance/");
  return res.data.map((r) => ({
    ...r,
    employee_name: r.employee_name || "موظف",
    site_name: r.site_name || "-",
    status: r.status || "حاضر",
  }));
}

export async function createAttendance(data) {
  try {
    const payload = {
      ...data,
      employee_id: Number(data.employee_id),
    };
    const res = await axiosInstance.post("/attendance/", payload);
    return res.data;
  } catch (err) {
    throw new Error(getErrorMessage(err, "فشل تسجيل الحضور"));
  }
}

export async function importEmployeesFromExcel(file, commit = true) {
  const formData = new FormData();
  formData.append("file", file);
  try {
    const res = await axiosInstance.post(`/imports/employees/?commit=${commit}`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return res.data;
  } catch (err) {
    throw new Error(getErrorMessage(err, "فشل الاستيراد"));
  }
}

export async function fetchSalaryReports() {
  const res = await axiosInstance.get("/reports/salary");
  return res.data;
}

export async function fetchAttendanceStats() {
  const res = await axiosInstance.get("/reports/attendance");
  return res.data;
}

export async function fetchDashboardStats() {
  const [employees, attendanceReport, salaryReport] = await Promise.all([
    fetchEmployees(),
    fetchAttendanceStats(),
    fetchSalaryReports(),
  ]);

  const salaryTotal = salaryReport.reduce((sum, row) => sum + Number(row.total || 0), 0);

  return {
    employeesCount: employees.length,
    attendancePercent: attendanceReport.percent_present || 0,
    salaryTotal,
  };
}
