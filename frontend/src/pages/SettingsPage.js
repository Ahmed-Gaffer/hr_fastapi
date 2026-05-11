import React, { useState, useEffect } from 'react';
import { Box, Button, Grid, TextField, Typography, Alert } from '@mui/material';

export default function SettingsPage() {
  const [apiBase, setApiBase] = useState('');
  const [tenantId, setTenantId] = useState('1');
  const [message, setMessage] = useState('');

  useEffect(() => {
    setApiBase(localStorage.getItem('apiBase') || 'http://192.168.10.92:8000/api');
    setTenantId(localStorage.getItem('tenantId') || '1');
  }, []);

  const handleSave = () => {
    localStorage.setItem('apiBase', apiBase);
    localStorage.setItem('tenantId', tenantId);
    setMessage('تم حفظ الإعدادات بنجاح');
  };

  const handleReset = () => {
    localStorage.removeItem('apiBase');
    localStorage.removeItem('tenantId');
    setApiBase('http://192.168.10.92:8000/api');
    setTenantId('1');
    setMessage('تمت إعادة الإعدادات الافتراضية');
  };

  return (
    <Box sx={{ mt: 10 }}>
      <Typography variant="h4" gutterBottom>الإعدادات العامة</Typography>
      {message && <Alert severity="success" sx={{ mb: 2 }}>{message}</Alert>}
      <Grid container spacing={2}>
        <Grid item xs={12} md={6}>
          <TextField
            label="عنوان API"
            value={apiBase}
            onChange={(e) => setApiBase(e.target.value)}
            fullWidth
          />
        </Grid>
        <Grid item xs={12} md={6}>
          <TextField
            label="معرف المستأجر"
            value={tenantId}
            onChange={(e) => setTenantId(e.target.value)}
            fullWidth
          />
        </Grid>
      </Grid>
      <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
        <Button variant="contained" onClick={handleSave}>حفظ</Button>
        <Button variant="outlined" onClick={handleReset}>إعادة ضبط</Button>
      </Box>
    </Box>
  );
}
