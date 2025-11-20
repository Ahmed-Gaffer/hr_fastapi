import React from 'react';
import { Box, Grid, Paper, Typography } from '@mui/material';
import { useTranslation } from 'react-i18next';

export default function Dashboard() {
  const { t } = useTranslation();
  return (
    <Box sx={{ mt: 10 }}>
      <Typography variant="h4" gutterBottom>{t('dashboard')}</Typography>
      <Grid container spacing={2}>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6">الموظفين</Typography>
            <Typography variant="h3">124</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6">الحضور اليوم</Typography>
            <Typography variant="h3">87%</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6">الرواتب هذا الشهر</Typography>
            <Typography variant="h3">৳ 240,000</Typography>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}