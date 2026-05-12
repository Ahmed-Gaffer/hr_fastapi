import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { useTranslation } from 'react-i18next'; // 1. استدعاء مكتبة الترجمة
import './i18n'; // 2. التأكد من استدعاء ملف الإعدادات بتاعك
import TopBar from './components/TopBar';
import SideBar from './components/SideBar';
import Dashboard from './pages/Dashboard';
import EmployeesPage from './pages/EmployeesPage';
import EmployeeDetailsPage from './pages/EmployeeDetailsPage';
import ImportPage from './pages/ImportPage';
import AttendancePage from './pages/AttendancePage';
import ReportsPage from './pages/ReportsPage';
import AdvancedAnalyticsPage from './pages/AdvancedAnalyticsPage';
import LoginPage from './pages/LoginPage';
import SalaryPage from './pages/SalaryPage';
import SalaryComponentsPage from './pages/SalaryComponentsPage';
import SitePage from './pages/SitePage';
import SystemPage from './pages/SystemPage';
import SettingsPage from './pages/SettingsPage';
import TenantsPage from './pages/TenantsPage';
import { Box } from '@mui/material';

export default function App() {
  const [open, setOpen] = React.useState(true);
  const { t } = useTranslation();                   // 3. تجهيز دالة الترجمة
  const token = localStorage.getItem('token');
  React.useEffect(() => {
    document.title = t('appTitle'); 
  }, [t]);                                      // 4. تغيير عنوان الصفحة للعربي من داخل الكود
  // إزالة شرط تسجيل الدخول للوصول المفتوح
  // if (!token) {
  //   return <LoginPage />;
  // }
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
          <Route path="/salary" element={<SalaryPage />} />
          <Route path="/salary-components" element={<SalaryComponentsPage />} />
          <Route path="/site" element={<SitePage />} />
          <Route path="/system" element={<SystemPage />} />
          <Route path="/settings" element={<SettingsPage />} />
          <Route path="/tenants" element={<TenantsPage />} />
          <Route path="/reports" element={<ReportsPage />} />
          <Route path="/analytics" element={<AdvancedAnalyticsPage />} />
          <Route path="/login" element={<LoginPage />} />
        </Routes>
      </Box>
    </BrowserRouter>
  );
}
