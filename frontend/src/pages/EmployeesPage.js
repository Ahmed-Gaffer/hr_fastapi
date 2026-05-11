import React, { useEffect, useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Grid,
  CircularProgress,
  Alert,
  Button,
  Stack,
  Table,
  TableHead,
  TableBody,
  TableCell,
  TableRow,
  Pagination,
  Paper,
  TableContainer,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { searchEmployees } from '../services/api';

export default function EmployeesPage() {
  const navigate = useNavigate();
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  // فلاتر
  const [searchQuery, setSearchQuery] = useState('');
  const [departmentId, setDepartmentId] = useState('');
  const [status, setStatus] = useState('');
  
  // pagination
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const pageSize = 50;

  const loadEmployees = async () => {
    setLoading(true);
    setError('');
    try {
      const filters = {};
      if (departmentId) filters.department_id = departmentId;
      if (status) filters.status = status;

      const skip = (page - 1) * pageSize;
      const result = await searchEmployees(searchQuery, filters, skip, pageSize);
      
      setEmployees(result.results);
      setTotal(result.total);
    } catch (err) {
      setError(err.message || 'فشل تحميل الموظفين');
    } finally {
      setLoading(false);
    }
  };

  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => {
    loadEmployees();
  }, [searchQuery, departmentId, status, page]);

  return (
    <Box sx={{ mt: 12, mb: 4 }}>
      <Typography variant="h4" gutterBottom>إدارة الموظفين</Typography>

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                placeholder="ابحث بالاسم أو الكود أو الرقم القومي..."
                value={searchQuery}
                onChange={(e) => {
                  setSearchQuery(e.target.value);
                  setPage(1);
                }}
                variant="outlined"
                size="small"
              />
            </Grid>
            <Grid item xs={12} md={2}>
              <FormControl fullWidth size="small">
                <InputLabel>القسم</InputLabel>
                <Select value={departmentId} label="القسم" onChange={(e) => {
                  setDepartmentId(e.target.value);
                  setPage(1);
                }}>
                  <MenuItem value="">الكل</MenuItem>
                  <MenuItem value="1">الإدارة</MenuItem>
                  <MenuItem value="2">الموارد البشرية</MenuItem>
                  <MenuItem value="3">المبيعات</MenuItem>
                  <MenuItem value="4">التشغيل</MenuItem>
                  <MenuItem value="5">الهندسة</MenuItem>
                  <MenuItem value="6">المحاسبة</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={2}>
              <FormControl fullWidth size="small">
                <InputLabel>الحالة</InputLabel>
                <Select value={status} label="الحالة" onChange={(e) => {
                  setStatus(e.target.value);
                  setPage(1);
                }}>
                  <MenuItem value="">الكل</MenuItem>
                  <MenuItem value="نشط">نشط</MenuItem>
                  <MenuItem value="موقوف">موقوف</MenuItem>
                  <MenuItem value="منتهي">منتهي</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={2}>
              <Button fullWidth variant="contained" onClick={loadEmployees} size="small">
                بحث
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {loading ? (
        <CircularProgress sx={{ display: 'block', mx: 'auto', mt: 4 }} />
      ) : error ? (
        <Alert severity="error">{error}</Alert>
      ) : (
        <>
          <Card>
            <CardContent>
              <Typography variant="subtitle2" sx={{ mb: 2 }}>
                إجمالي النتائج: {total}
              </Typography>
              <TableContainer component={Paper}>
                <Table>
                  <TableHead>
                    <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
                      <TableCell>الكود</TableCell>
                      <TableCell>الاسم</TableCell>
                      <TableCell>الوظيفة</TableCell>
                      <TableCell>القسم</TableCell>
                      <TableCell>الموقع</TableCell>
                      <TableCell>الراتب الأساسي</TableCell>
                      <TableCell>الحالة</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {employees.length === 0 ? (
                      <TableRow>
                        <TableCell colSpan={7} align="center">
                          لا توجد نتائج
                        </TableCell>
                      </TableRow>
                    ) : (
                      employees.map((emp) => (
                        <TableRow 
                          key={emp.id}
                          hover
                          onClick={() => navigate(`/employees/${emp.id}`)}
                          sx={{ cursor: 'pointer' }}
                        >
                          <TableCell>{emp.code}</TableCell>
                          <TableCell>{emp.name}</TableCell>
                          <TableCell>{emp.job_title || '-'}</TableCell>
                          <TableCell>{emp.department_name || '-'}</TableCell>
                          <TableCell>{emp.site_name || '-'}</TableCell>
                          <TableCell>{emp.base_salary?.toLocaleString?.() || 0}</TableCell>
                          <TableCell>{emp.status}</TableCell>
                        </TableRow>
                      ))
                    )}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>

          <Stack direction="row" justifyContent="center" sx={{ mt: 3 }}>
            <Pagination
              count={Math.ceil(total / pageSize)}
              page={page}
              onChange={(e, value) => setPage(value)}
              color="primary"
            />
          </Stack>
        </>
      )}
    </Box>
  );
}
