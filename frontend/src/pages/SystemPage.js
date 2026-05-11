import React, { useState, useEffect } from 'react';
import { TextField, Button, Box, Typography, Grid, Switch, FormControlLabel } from '@mui/material';
import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || "http://192.168.10.92:8000/api";

const axiosInstance = axios.create({ baseURL: API_BASE });
axiosInstance.interceptors.request.use((config) => {
  config.headers["X-Tenant-ID"] = localStorage.getItem("tenantId") || "1";
  const token = localStorage.getItem('token');
  if (token) {
    config.headers["Authorization"] = `Bearer ${token}`;
  }
  return config;
});

export default function SystemPage() {
  const [config, setConfig] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadConfig();
  }, []);

  const loadConfig = async () => {
    try {
      const res = await axiosInstance.get('/system/config');
      setConfig(res.data);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  const handleChange = (field, value) => {
    setConfig({ ...config, [field]: value });
  };

  const handleSave = async () => {
    try {
      await axiosInstance.put('/system/config', config);
      alert('تم حفظ الإعدادات');
    } catch (err) {
      console.error(err);
      alert('فشل في الحفظ');
    }
  };

  if (loading) return <div>جاري التحميل...</div>;

  return (
    <Box>
      <Typography variant="h4" gutterBottom>إعدادات النظام</Typography>
      <Grid container spacing={2}>
        <Grid item xs={12} sm={6}>
          <TextField
            label="الإعفاء الشخصي السنوي"
            type="number"
            value={config.personal_exemption_annual || ''}
            onChange={(e) => handleChange('personal_exemption_annual', parseFloat(e.target.value))}
            fullWidth
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            label="معدل التأمين الاجتماعي للموظف"
            type="number"
            value={config.insurance_social_employee_rate || ''}
            onChange={(e) => handleChange('insurance_social_employee_rate', parseFloat(e.target.value))}
            fullWidth
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            label="معدل التأمين الصحي"
            type="number"
            value={config.insurance_health_rate || ''}
            onChange={(e) => handleChange('insurance_health_rate', parseFloat(e.target.value))}
            fullWidth
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            label="معدل التأمين الاجتماعي لصاحب العمل"
            type="number"
            value={config.insurance_employer_social_rate || ''}
            onChange={(e) => handleChange('insurance_employer_social_rate', parseFloat(e.target.value))}
            fullWidth
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            label="معدل التأمين الصحي لصاحب العمل"
            type="number"
            value={config.insurance_employer_health_rate || ''}
            onChange={(e) => handleChange('insurance_employer_health_rate', parseFloat(e.target.value))}
            fullWidth
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            label="مضاعف الساعات الإضافية النهارية"
            type="number"
            value={config.day_overtime_multiplier || ''}
            onChange={(e) => handleChange('day_overtime_multiplier', parseFloat(e.target.value))}
            fullWidth
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            label="مضاعف الساعات الإضافية الليلية"
            type="number"
            value={config.night_overtime_multiplier || ''}
            onChange={(e) => handleChange('night_overtime_multiplier', parseFloat(e.target.value))}
            fullWidth
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            label="نوع خصم الغياب"
            value={config.absence_deduction_type || ''}
            onChange={(e) => handleChange('absence_deduction_type', e.target.value)}
            fullWidth
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            label="قيمة خصم الغياب"
            type="number"
            value={config.absence_deduction_value || ''}
            onChange={(e) => handleChange('absence_deduction_value', parseFloat(e.target.value))}
            fullWidth
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <FormControlLabel
            control={
              <Switch
                checked={config.minimum_salary_enabled || false}
                onChange={(e) => handleChange('minimum_salary_enabled', e.target.checked)}
              />
            }
            label="تفعيل الحد الأدنى للراتب"
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            label="الحد الأدنى للراتب"
            type="number"
            value={config.minimum_salary || ''}
            onChange={(e) => handleChange('minimum_salary', parseFloat(e.target.value))}
            fullWidth
            disabled={!config.minimum_salary_enabled}
          />
        </Grid>
      </Grid>
      <Box mt={2}>
        <Button variant="contained" onClick={handleSave}>حفظ الإعدادات</Button>
      </Box>
    </Box>
  );
}