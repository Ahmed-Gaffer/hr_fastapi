import axios from "axios";

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";
const axiosInstance = axios.create({ baseURL: API_BASE });

// Employees
export async function fetchEmployees() {
  try {
    const res = await axiosInstance.get("/employees");
    return res.data.map((e) => ({
      id: e.id,
      name: e.name || e.full_name || "—",
      role: e.role || "-",
      site: e.site_name || "-",
    }));
  } catch (err) {
    console.error("fetchEmployees error:", err.response ? err.response.data : err.message);
    return [{ id: 1, name: "أحمد محمد", role: "مهندس", site: "القاهرة" }];
  }
}

export async function fetchEmployee(id) {
  try {
    const res = await axiosInstance.get(`/employees/${id}`);
    return res.data;
  } catch {
    return { id, name: "موظف", email: "email@example.com", phone: "0123456789", role: "موظف", site: "الموقع", hire_date: "2023-01-01", base_salary: 5000 };
  }
}

// Attendance
export async function fetchAttendanceRecords() {
  try {
    const res = await axiosInstance.get("/attendance");
    return res.data.map((r) => ({
      id: r.id,
      employee_name: r.employee?.name || "موظف",
      date: r.date,
      status: r.status || "حاضر",
    }));
  } catch {
    return [];
  }
}

export async function recordAttendance(data) {
  try {
    const res = await axiosInstance.post("/attendance", data);
    return res.data;
  } catch (err) {
    throw new Error(err.response?.data?.detail || "فشل تسجيل الحضور");
  }
}

// Import
export async function importEmployeesFromExcel(file) {
  const formData = new FormData();
  formData.append("file", file);
  try {
    const res = await axiosInstance.post("/import", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return { count: res.data.imported || 0 };
  } catch (err) {
    throw new Error(err.response?.data?.detail || "فشل الاستيراد");
  }
}

// Reports
export async function fetchSalaryReports() {
  try {
    const res = await axiosInstance.get("/reports/salary");
    return res.data;
  } catch {
    return [
      { month: "يناير", total: 100000, department: "IT" },
      { month: "فبراير", total: 105000, department: "HR" },
    ];
  }
}

export async function fetchAttendanceStats() {
  try {
    const res = await axiosInstance.get("/reports/attendance");
    return res.data;
  } catch {
    return [
      { name: "حاضر", value: 80 },
      { name: "غائب", value: 15 },
      { name: "إجازة", value: 5 },
    ];
  }
}
