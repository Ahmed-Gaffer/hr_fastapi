import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Box, Card, CardContent, Typography, Grid, Button, CircularProgress, Alert } from '@mui/material';
import { fetchEmployee } from '../services/api';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';

export default function EmployeeDetailsPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [employee, setEmployee] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchEmployee(id)
      .then(data => {
        setEmployee(data);
        setLoading(false);
      })
      .catch(err => {
        setError('فشل تحميل بيانات الموظف');
        setLoading(false);
      });
  }, [id]);

  if (loading) return <CircularProgress sx={{ mt: 20 }} />;
  if (error) return <Alert severity="error" sx={{ mt: 20 }}>{error}</Alert>;
  if (!employee) return <Alert severity="warning" sx={{ mt: 20 }}>لم يتم العثور على الموظف</Alert>;

  return (
    <Box sx={{ mt: 12, mb: 4 }}>
      <Button startIcon={<ArrowBackIcon />} onClick={() => navigate('/employees')} sx={{ mb: 2 }}>
        العودة
      </Button>
      <Card>
        <CardContent>
          <Typography variant="h4" gutterBottom>{employee.name}</Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <Typography color="textSecondary">البريد الإلكتروني</Typography>
              <Typography variant="body1">{employee.email || 'غير محدد'}</Typography>
            </Grid>
            <Grid item xs={12} md={6}>
              <Typography color="textSecondary">الهاتف</Typography>
              <Typography variant="body1">{employee.phone || 'غير محدد'}</Typography>
            </Grid>
            <Grid item xs={12} md={6}>
              <Typography color="textSecondary">المنصب</Typography>
              <Typography variant="body1">{employee.role || 'غير محدد'}</Typography>
            </Grid>
            <Grid item xs={12} md={6}>
              <Typography color="textSecondary">الموقع</Typography>
              <Typography variant="body1">{employee.site || 'غير محدد'}</Typography>
            </Grid>
            <Grid item xs={12} md={6}>
              <Typography color="textSecondary">تاريخ التوظيف</Typography>
              <Typography variant="body1">{employee.hire_date || 'غير محدد'}</Typography>
            </Grid>
            <Grid item xs={12} md={6}>
              <Typography color="textSecondary">الراتب الأساسي</Typography>
              <Typography variant="body1">{employee.base_salary ? `${employee.base_salary} ج.م` : 'غير محدد'}</Typography>
            </Grid>
          </Grid>
        </CardContent>
      </Card>
    </Box>
  );
}