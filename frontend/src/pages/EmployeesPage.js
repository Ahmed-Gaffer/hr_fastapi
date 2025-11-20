import React, { useEffect, useState } from "react";
import { getEmployees, addEmployee, updateEmployee, deleteEmployee } from "../services/api";

function EmployeesPage() {
  const [employees, setEmployees] = useState([]);
  const [newEmployee, setNewEmployee] = useState({ name: "", phone: "" });

  useEffect(() => {
    getEmployees().then(data => setEmployees(data));
  }, []);

  const handleAdd = async () => {
    const added = await addEmployee(newEmployee);
    setEmployees([...employees, added]);
    setNewEmployee({ name: "", phone: "" });
  };

  const handleDelete = async (id) => {
    await deleteEmployee(id);
    setEmployees(employees.filter(emp => emp.id !== id));
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>👥 قائمة الموظفين</h1>
      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>الاسم</th>
            <th>الهاتف</th>
            <th>إجراءات</th>
          </tr>
        </thead>
        <tbody>
          {employees.map(emp => (
            <tr key={emp.id}>
              <td>{emp.name}</td>
              <td>{emp.phone}</td>
              <td>
                <button onClick={() => handleDelete(emp.id)}>🗑 حذف</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2>➕ إضافة موظف جديد</h2>
      <input
        type="text"
        placeholder="الاسم"
        value={newEmployee.name}
        onChange={e => setNewEmployee({ ...newEmployee, name: e.target.value })}
      />
      <input
        type="text"
        placeholder="الهاتف"
        value={newEmployee.phone}
        onChange={e => setNewEmployee({ ...newEmployee, phone: e.target.value })}
      />
      <button onClick={handleAdd}>إضافة</button>
    </div>
  );
}

export default EmployeesPage;
