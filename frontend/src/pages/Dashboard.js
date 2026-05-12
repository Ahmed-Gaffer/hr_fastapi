import React, { useEffect, useState } from 'react';
import { Alert, Box, CircularProgress, Grid, Paper, Typography, Card, CardContent } from '@mui/material';
import { useTranslation } from 'react-i18next';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, PieChart, Pie, Cell, LineChart, Line, ResponsiveContainer } from 'recharts';
import { fetchDashboardStats } from '../services/api';

export default function Dashboard() {
  const { t } = useTranslation();
  const [stats, setStats] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboardStats()
      .then(setStats)
      .catch((err) => setError(err.message || 'فشل تحميل لوحة التحكم'));
  }, []);

  if (error) return <Alert severity="error" sx={{ mt: 10 }}>{error}</Alert>;
  if (!stats) return <CircularProgress sx={{ mt: 20 }} />;

  // Sample data for charts (replace with real data from API)
  const departmentData = [
    { name: 'الإدارة', value: 10 },
    { name: 'المحاسبة', value: 15 },
    { name: 'التسويق', value: 8 },
    { name: 'التقنية', value: 20 },
  ];

  const attendanceData = [
    { month: 'يناير', حضور: 95, غياب: 5 },
    { month: 'فبراير', حضور: 92, غياب: 8 },
    { month: 'مارس', حضور: 98, غياب: 2 },
    { month: 'أبريل', حضور: 96, غياب: 4 },
  ];

  const salaryData = [
    { month: 'يناير', salary: 50000 },
    { month: 'فبراير', salary: 52000 },
    { month: 'مارس', salary: 48000 },
    { month: 'أبريل', salary: 55000 },
  ];

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

  return (
    <Box sx={{ mt: 10, p: 3, backgroundColor: '#f5f5f5', minHeight: '100vh' }}>
      <Typography variant="h4" gutterBottom sx={{ mb: 3, fontWeight: 'bold' }}>
        لوحة التحكم الرئيسية
      </Typography>

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)', color: 'white', boxShadow: 3 }}>
            <CardContent>
              <Typography variant="h6">إجمالي الموظفين</Typography>
              <Typography variant="h3">{stats.employeesCount}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ background: 'linear-gradient(45deg, #4CAF50 30%, #81C784 90%)', color: 'white', boxShadow: 3 }}>
            <CardContent>
              <Typography variant="h6">نسبة الحضور</Typography>
              <Typography variant="h3">{stats.attendancePercent}%</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ background: 'linear-gradient(45deg, #FF9800 30%, #FFB74D 90%)', color: 'white', boxShadow: 3 }}>
            <CardContent>
              <Typography variant="h6">إجمالي الرواتب</Typography>
              <Typography variant="h3">{stats.salaryTotal.toLocaleString('ar-EG')} ج.م</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ background: 'linear-gradient(45deg, #F44336 30%, #EF5350 90%)', color: 'white', boxShadow: 3 }}>
            <CardContent>
              <Typography variant="h6">الإجازات المعلقة</Typography>
              <Typography variant="h3">12</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Charts Row 1 */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={6}>
          <Card sx={{ boxShadow: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>توزيع الموظفين حسب القسم</Typography>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={departmentData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {departmentData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={6}>
          <Card sx={{ boxShadow: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>إحصائيات الحضور والغياب</Typography>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={attendanceData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="حضور" fill="#4CAF50" />
                  <Bar dataKey="غياب" fill="#F44336" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Charts Row 2 */}
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Card sx={{ boxShadow: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>تطور إجمالي الرواتب</Typography>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={salaryData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="salary" stroke="#2196F3" strokeWidth={3} />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}
