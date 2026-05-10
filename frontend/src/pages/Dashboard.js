import React, { useEffect, useState } from 'react';
import { Alert, Box, CircularProgress, Grid, Paper, Typography } from '@mui/material';
import { useTranslation } from 'react-i18next';
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

  return (
    <Box sx={{ mt: 10 }}>
      <Typography variant="h4" gutterBottom>{t('dashboard')}</Typography>
      <Grid container spacing={2}>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6">الموظفين</Typography>
            <Typography variant="h3">{stats.employeesCount}</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6">نسبة الحضور</Typography>
            <Typography variant="h3">{stats.attendancePercent}%</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6">إجمالي الرواتب</Typography>
            <Typography variant="h3">{stats.salaryTotal.toLocaleString('ar-EG')} ج.م</Typography>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}
