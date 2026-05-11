import axios from "axios";

const getApiBase = () =>
  localStorage.getItem("apiBase") || process.env.REACT_APP_API_URL || "http://192.168.10.92:8000/api";

const getTenantId = () =>
  localStorage.getItem("tenantId") || process.env.REACT_APP_TENANT_ID || "1";

const axiosInstance = axios.create();

axiosInstance.interceptors.request.use((config) => {
  config.baseURL = getApiBase();
  config.headers["X-Tenant-ID"] = getTenantId();
  const token = localStorage.getItem('token');
  if (token) {
    config.headers["Authorization"] = `Bearer ${token}`;
  }
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

export async function fetchSalaries() {
  const res = await axiosInstance.get("/salary/");
  return res.data;
}
export async function fetchSalaryByDepartment() {
  const res = await axiosInstance.get("/reports/salary/by-department");
  return res.data;
}

export async function fetchSalaryByCostCenter() {
  const res = await axiosInstance.get("/reports/salary/by-cost-center");
  return res.data;
}

export async function fetchAttendanceBySite() {
  const res = await axiosInstance.get("/reports/attendance/by-site");
  return res.data;
}

export async function fetchAttendanceByCostCenter() {
  const res = await axiosInstance.get("/reports/attendance/by-cost-center");
  return res.data;
}

export async function fetchSalaryBySite() {
  const res = await axiosInstance.get("/reports/salary/by-site");
  return res.data;
}

export async function fetchEmployeesByDepartment() {
  const res = await axiosInstance.get("/reports/employees/by-department");
  return res.data;
}

export async function fetchEmployeesBySite() {
  const res = await axiosInstance.get("/reports/employees/by-site");
  return res.data;
}

export async function fetchEmployeesByCostCenter() {
  const res = await axiosInstance.get("/reports/employees/by-cost-center");
  return res.data;
}

export async function fetchEmployeesByJobTitle() {
  const res = await axiosInstance.get("/reports/employees/by-job-title");
  return res.data;
}

export async function fetchEmployeesWithoutDepartment() {
  const res = await axiosInstance.get("/reports/employees/without-department");
  return res.data;
}

export async function fetchOvertimeSummary() {
  const res = await axiosInstance.get("/reports/overtime/summary");
  return res.data;
}
export async function searchEmployees(q, filters = {}, skip = 0, limit = 50) {
  const params = new URLSearchParams({ q, skip, limit, ...filters });
  const res = await axiosInstance.get(`/search/employees?${params}`);
  return res.data;
}

export async function searchSalaries(filters = {}, skip = 0, limit = 50) {
  const params = new URLSearchParams({ skip, limit, ...filters });
  const res = await axiosInstance.get(`/search/salaries?${params}`);
  return res.data;
}

export async function searchAttendance(filters = {}, skip = 0, limit = 50) {
  const params = new URLSearchParams({ skip, limit, ...filters });
  const res = await axiosInstance.get(`/search/attendance?${params}`);
  return res.data;
}

export async function fetchPayrollSummary(year, month) {
  const params = new URLSearchParams();
  if (year) params.append("year", year);
  if (month) params.append("month", month);
  const res = await axiosInstance.get(`/analytics/payroll-summary?${params}`);
  return res.data;
}

export async function fetchAttendanceSummary(fromDate, toDate) {
  const params = new URLSearchParams();
  if (fromDate) params.append("from_date", fromDate);
  if (toDate) params.append("to_date", toDate);
  const res = await axiosInstance.get(`/analytics/attendance-summary?${params}`);
  return res.data;
}

export async function fetchEmployeePerformance(year, month, departmentId, skip = 0, limit = 100) {
  const params = new URLSearchParams({ skip, limit });
  if (year) params.append("year", year);
  if (month) params.append("month", month);
  if (departmentId) params.append("department_id", departmentId);
  const res = await axiosInstance.get(`/analytics/employee-performance?${params}`);
  return res.data;
}

export async function fetchDepartmentAnalysis(year, month) {
  const params = new URLSearchParams();
  if (year) params.append("year", year);
  if (month) params.append("month", month);
  const res = await axiosInstance.get(`/analytics/department-analysis?${params}`);
  return res.data;
}

export async function fetchCostCenterAnalysis(year, month) {
  const params = new URLSearchParams();
  if (year) params.append("year", year);
  if (month) params.append("month", month);
  const res = await axiosInstance.get(`/analytics/cost-center-analysis?${params}`);
  return res.data;
}

export async function createSalary(data) {
  try {
    const payload = {
      ...data,
      employee_id: Number(data.employee_id),
      amount: Number(data.amount),
      month: Number(data.month),
      year: Number(data.year),
    };
    const res = await axiosInstance.post("/salary/", payload);
    return res.data;
  } catch (err) {
    throw new Error(getErrorMessage(err, "فشل إضافة الراتب"));
  }
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
