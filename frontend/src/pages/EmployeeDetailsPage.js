import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Box, Card, CardContent, Typography, Grid, Button, CircularProgress, Alert } from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import { fetchEmployee } from '../services/api';

export default function EmployeeDetailsPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [employee, setEmployee] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchEmployee(id)
      .then((data) => {
        setEmployee(data);
        setLoading(false);
      })
      .catch(() => {
        setError('فشل تحميل بيانات الموظف');
        setLoading(false);
      });
  }, [id]);

  if (loading) return <CircularProgress sx={{ mt: 20 }} />;
  if (error) return <Alert severity="error" sx={{ mt: 20 }}>{error}</Alert>;
  if (!employee) return <Alert severity="warning" sx={{ mt: 20 }}>لم يتم العثور على الموظف</Alert>;

  const fields = [
    ['الكود', employee.code],
    ['الوظيفة', employee.job_title],
    ['الموقع', employee.site_name],
    ['مركز التكلفة', employee.cost_center_name],
    ['القسم', employee.department_name],
    ['تاريخ التعيين', employee.hire_date],
    ['الرقم القومي', employee.national_id],
    ['الراتب الأساسي', employee.base_salary ? `${employee.base_salary} ج.م` : null],
    ['حالة العمل', employee.work_status],
    ['حالة الموظف', employee.status],
  ];

  return (
    <Box sx={{ mt: 12, mb: 4 }}>
      <Button startIcon={<ArrowBackIcon />} onClick={() => navigate('/employees')} sx={{ mb: 2 }}>
        العودة
      </Button>
      <Card>
        <CardContent>
          <Typography variant="h4" gutterBottom>{employee.name}</Typography>
          <Grid container spacing={2}>
            {fields.map(([label, value]) => (
              <Grid item xs={12} md={6} key={label}>
                <Typography color="text.secondary">{label}</Typography>
                <Typography variant="body1">{value || 'غير محدد'}</Typography>
              </Grid>
            ))}
          </Grid>
        </CardContent>
      </Card>
    </Box>
  );
}
