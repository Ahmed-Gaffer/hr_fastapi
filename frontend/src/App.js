import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import TopBar from './components/TopBar';
import SideBar from './components/SideBar';
import Dashboard from './pages/Dashboard';
import EmployeesPage from './pages/EmployeesPage';
import EmployeeDetailsPage from './pages/EmployeeDetailsPage';
import ImportPage from './pages/ImportPage';
import AttendancePage from './pages/AttendancePage';
import ReportsPage from './pages/ReportsPage';
import { Box } from '@mui/material';

export default function App() {
  const [open, setOpen] = React.useState(true);
  return (
    <BrowserRouter>
      <TopBar open={open} setOpen={setOpen} />
      <SideBar open={open} setOpen={setOpen} />
      <Box component="main" sx={{ p: 3, marginRight: open ? '240px' : '72px', transition: 'margin .2s', minHeight: '100vh' }}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/employees" element={<EmployeesPage />} />
          <Route path="/employees/:id" element={<EmployeeDetailsPage />} />
          <Route path="/import" element={<ImportPage />} />
          <Route path="/attendance" element={<AttendancePage />} />
          <Route path="/reports" element={<ReportsPage />} />
        </Routes>
      </Box>
    </BrowserRouter>
  );
}
