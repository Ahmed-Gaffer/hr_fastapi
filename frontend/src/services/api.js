import axios from "axios";

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";
const axiosInstance = axios.create({ baseURL: API_BASE });

// ======================= Employees =======================
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
    // بيانات افتراضية لو السيرفر وقع
    return [{ id: 1, name: "أحمد محمد", role: "مهندس", site: "القاهرة" }];
  }
}

export async function fetchEmployee(id) {
  try {
    const res = await axiosInstance.get(`/employees/${id}`);
    return res.data;
  } catch (err) {
    console.error("fetchEmployee error:", err.response ? err.response.data : err.message);
    // بيانات افتراضية
    return {
      id,
      name: "موظف",
      email: "email@example.com",
      phone: "0123456789",
      role: "موظف",
      site: "الموقع",
      hire_date: "2023-01-01",
      base_salary: 5000,
    };
  }
}

// ======================= Attendance =======================
export async function fetchAttendances() {
  try {
    const res = await axiosInstance.get("/attendance");
    return res.data.map((r) => ({
      id: r.id,
      employee_name: r.employee?.name || "موظف",
      date: r.date,
      status: r.status || "حاضر",
    }));
  } catch (err) {
    console.error("fetchAttendances error:", err.response ? err.response.data : err.message);
    return [];
  }
}

export async function Attendance(data) {
  try {
    const res = await axiosInstance.post("/attendance", data);
    return res.data;
  } catch (err) {
    const errorMsg =
      err.response?.data?.detail ||
      err.response?.data?.error ||
      err.message ||
      "فشل تسجيل الحضور";
    throw new Error(errorMsg);
  }
}

// ======================= Import =======================
export async function importEmployeesFromExcel(file, commit = false) {
  const formData = new FormData();
  formData.append("file", file);
  try {
    const res = await axiosInstance.post(`/import/bulk?commit=${commit}`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return res.data; // هيكون فيه status و count أو تفاصيل التقرير
  } catch (err) {
    const errorMsg =
      err.response?.data?.detail ||
      err.response?.data?.error ||
      err.message ||
      "فشل الاستيراد";
    throw new Error(errorMsg);
  }
}

// ======================= Reports =======================
export async function fetchSalaryReports() {
  try {
    const res = await axiosInstance.get("/reports/salary");
    return res.data;
  } catch (err) {
    const errorMsg =
      err.response?.data?.detail ||
      err.response?.data?.error ||
      err.message ||
      "فشل جلب تقارير الرواتب";

    console.error("fetchSalaryReports error:", errorMsg);

    // بيانات افتراضية لو السيرفر وقع
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
  } catch (err) {
    console.error("fetchAttendanceStats error:", err.response ? err.response.data : err.message);
    return [
      { name: "حاضر", value: 80 },
      { name: "غائب", value: 15 },
      { name: "إجازة", value: 5 },
    ];
  }
}
