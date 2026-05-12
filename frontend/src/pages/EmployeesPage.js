import React, { useCallback, useEffect, useState } from 'react';
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
  Chip,
  Fab,
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import FilterListIcon from '@mui/icons-material/FilterList';
import GetAppIcon from '@mui/icons-material/GetApp';
import { useNavigate } from 'react-router-dom';
import * as XLSX from 'xlsx';
import { searchEmployees, fetchSites, fetchDepartments, fetchCostCenters } from '../services/api';

export default function EmployeesPage() {
  const navigate = useNavigate();
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  // فلاتر
  const [searchQuery, setSearchQuery] = useState('');
  const [departmentId, setDepartmentId] = useState('');
  const [siteId, setSiteId] = useState('');
  const [costCenterId, setCostCenterId] = useState('');
  const [status, setStatus] = useState('');
  const [workStatus, setWorkStatus] = useState('');
  const [insuranceStatus, setInsuranceStatus] = useState('');
  const [employeeCategory, setEmployeeCategory] = useState('');
  const [sites, setSites] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [costCenters, setCostCenters] = useState([]);
  
  // pagination
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const pageSize = 50;

  // sorting
  const [sortBy, setSortBy] = useState('name');
  const [sortOrder, setSortOrder] = useState('asc');

  const loadEmployees = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const filters = {};
      if (departmentId) filters.department_id = departmentId;
      if (siteId) filters.site_id = siteId;
      if (costCenterId) filters.cost_center_id = costCenterId;
      if (status) filters.status = status;
      if (workStatus) filters.work_status = workStatus;
      if (insuranceStatus) filters.insurance_status = insuranceStatus;
      if (employeeCategory) filters.employee_category = employeeCategory;

      const skip = (page - 1) * pageSize;
      const result = await searchEmployees(searchQuery, filters, skip, pageSize);
      
      setEmployees(result.results);
      setTotal(result.total);
    } catch (err) {
      setError(err.message || 'فشل تحميل الموظفين');
    } finally {
      setLoading(false);
    }
  }, [costCenterId, departmentId, employeeCategory, insuranceStatus, page, pageSize, searchQuery, siteId, status, workStatus]);

  useEffect(() => {
    loadEmployees();
  }, [loadEmployees]);

  useEffect(() => {
    const loadFilters = async () => {
      try {
        const [sitesData, departmentsData, costCentersData] = await Promise.all([
          fetchSites(),
          fetchDepartments(),
          fetchCostCenters(),
        ]);
        setSites(sitesData);
        setDepartments(departmentsData);
        setCostCenters(costCentersData);
      } catch (err) {
        console.error('Failed to load filter options', err);
      }
    };

    loadFilters();
  }, []);

  const handleSort = (field) => {
    if (sortBy === field) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(field);
      setSortOrder('asc');
    }
    // Re-sort the current employees array
    const sorted = [...employees].sort((a, b) => {
      const aVal = a[field] || '';
      const bVal = b[field] || '';
      if (sortOrder === 'asc') {
        return aVal.localeCompare(bVal);
      } else {
        return bVal.localeCompare(aVal);
      }
    });
    setEmployees(sorted);
  };

  const handleExport = () => {
    const ws = XLSX.utils.json_to_sheet(employees);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Employees');
    XLSX.writeFile(wb, 'employees.xlsx');
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'نشط':
        return 'success';
      case 'موقوف':
        return 'warning';
      case 'منتهي':
        return 'error';
      default:
        return 'default';
    }
  };

  const resetFilters = () => {
    setSearchQuery('');
    setDepartmentId('');
    setSiteId('');
    setCostCenterId('');
    setStatus('');
    setWorkStatus('');
    setInsuranceStatus('');
    setEmployeeCategory('');
    setPage(1);
  };

  return (
    <Box sx={{ p: 3, backgroundColor: '#f5f5f5', minHeight: '100vh' }}>
      {/* Header Stats */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)', color: 'white' }}>
            <CardContent>
              <Typography variant="h6">إجمالي الموظفين</Typography>
              <Typography variant="h4">{total}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ background: 'linear-gradient(45deg, #4CAF50 30%, #81C784 90%)', color: 'white' }}>
            <CardContent>
              <Typography variant="h6">نشط</Typography>
              <Typography variant="h4">{employees.filter(e => e.status === 'نشط').length}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ background: 'linear-gradient(45deg, #FF9800 30%, #FFB74D 90%)', color: 'white' }}>
            <CardContent>
              <Typography variant="h6">موقوف</Typography>
              <Typography variant="h4">{employees.filter(e => e.status === 'موقوف').length}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ background: 'linear-gradient(45deg, #F44336 30%, #EF5350 90%)', color: 'white' }}>
            <CardContent>
              <Typography variant="h6">منتهي</Typography>
              <Typography variant="h4">{employees.filter(e => e.status === 'منتهي').length}</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Card sx={{ mb: 3, boxShadow: 3 }}>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center' }}>
            <FilterListIcon sx={{ mr: 1 }} />
            فلاتر البحث
          </Typography>
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
            <Grid item xs={12} md={3}>
              <FormControl fullWidth size="small">
                <InputLabel>الموقع</InputLabel>
                <Select value={siteId} label="الموقع" onChange={(e) => {
                  setSiteId(e.target.value);
                  setPage(1);
                }}>
                  <MenuItem value="">الكل</MenuItem>
                  {sites.map((site) => (
                    <MenuItem key={site.id} value={site.id}>{site.name}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={3}>
              <FormControl fullWidth size="small">
                <InputLabel>القسم</InputLabel>
                <Select value={departmentId} label="القسم" onChange={(e) => {
                  setDepartmentId(e.target.value);
                  setPage(1);
                }}>
                  <MenuItem value="">الكل</MenuItem>
                  {departments.map((dept) => (
                    <MenuItem key={dept.id} value={dept.id}>{dept.name}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={12} md={3}>
              <FormControl fullWidth size="small">
                <InputLabel>مركز التكلفة</InputLabel>
                <Select value={costCenterId} label="مركز التكلفة" onChange={(e) => {
                  setCostCenterId(e.target.value);
                  setPage(1);
                }}>
                  <MenuItem value="">الكل</MenuItem>
                  {costCenters.map((center) => (
                    <MenuItem key={center.id} value={center.id}>{center.name}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={3}>
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
            <Grid item xs={12} md={3}>
              <FormControl fullWidth size="small">
                <InputLabel>حالة العمل</InputLabel>
                <Select value={workStatus} label="حالة العمل" onChange={(e) => {
                  setWorkStatus(e.target.value);
                  setPage(1);
                }}>
                  <MenuItem value="">الكل</MenuItem>
                  <MenuItem value="يعمل">يعمل</MenuItem>
                  <MenuItem value="اجازة بدون مرتب">اجازة بدون مرتب</MenuItem>
                  <MenuItem value="موقوف">موقوف</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={3}>
              <FormControl fullWidth size="small">
                <InputLabel>حالة التأمين</InputLabel>
                <Select value={insuranceStatus} label="حالة التأمين" onChange={(e) => {
                  setInsuranceStatus(e.target.value);
                  setPage(1);
                }}>
                  <MenuItem value="">الكل</MenuItem>
                  <MenuItem value="مؤمن">مؤمن</MenuItem>
                  <MenuItem value="غير مؤمن">غير مؤمن</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={3}>
              <TextField
                fullWidth
                size="small"
                label="فئة الموظف"
                value={employeeCategory}
                onChange={(e) => {
                  setEmployeeCategory(e.target.value);
                  setPage(1);
                }}
              />
            </Grid>
            <Grid item xs={12} md={3}>
              <Stack direction="row" spacing={1}>
                <Button fullWidth variant="contained" onClick={loadEmployees} size="small">
                  بحث
                </Button>
                <Button
                  fullWidth
                  variant="outlined"
                  onClick={resetFilters}
                  size="small"
                >
                  مسح
                </Button>
                <Button variant="contained" onClick={handleExport} startIcon={<GetAppIcon />} size="small">
                  تصدير
                </Button>
              </Stack>
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
              <TableContainer component={Paper} sx={{ maxHeight: 600 }}>
                <Table stickyHeader>
                  <TableHead>
                    <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
                      <TableCell onClick={() => handleSort('code')} sx={{ cursor: 'pointer', fontWeight: 'bold' }}>
                        الكود {sortBy === 'code' && (sortOrder === 'asc' ? '↑' : '↓')}
                      </TableCell>
                      <TableCell onClick={() => handleSort('name')} sx={{ cursor: 'pointer', fontWeight: 'bold' }}>
                        الاسم {sortBy === 'name' && (sortOrder === 'asc' ? '↑' : '↓')}
                      </TableCell>
                      <TableCell onClick={() => handleSort('job_title')} sx={{ cursor: 'pointer', fontWeight: 'bold' }}>
                        الوظيفة {sortBy === 'job_title' && (sortOrder === 'asc' ? '↑' : '↓')}
                      </TableCell>
                      <TableCell>القسم</TableCell>
                      <TableCell>الموقع</TableCell>
                      <TableCell>مركز التكلفة</TableCell>
                      <TableCell>حالة العمل</TableCell>
                      <TableCell>التأمين</TableCell>
                      <TableCell>الفئة</TableCell>
                      <TableCell>الحالة</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {employees.length === 0 ? (
                      <TableRow>
                        <TableCell colSpan={10} align="center">
                          لا توجد نتائج
                        </TableCell>
                      </TableRow>
                    ) : (
                      employees.map((emp) => (
                        <TableRow 
                          key={emp.id}
                          hover
                          onClick={() => navigate(`/employees/${emp.id}`)}
                          sx={{ cursor: 'pointer', '&:hover': { backgroundColor: '#f9f9f9' } }}
                        >
                          <TableCell>{emp.code}</TableCell>
                          <TableCell>
                            <Typography variant="body2" fontWeight="bold">{emp.name}</Typography>
                          </TableCell>
                          <TableCell>{emp.job_title || '-'}</TableCell>
                          <TableCell>{emp.department_name || '-'}</TableCell>
                          <TableCell>{emp.site_name || '-'}</TableCell>
                          <TableCell>{emp.cost_center_name || '-'}</TableCell>
                          <TableCell>{emp.work_status || '-'}</TableCell>
                          <TableCell>{emp.insurance_status || '-'}</TableCell>
                          <TableCell>{emp.employee_category || '-'}</TableCell>
                          <TableCell>
                            <Chip label={emp.status} color={getStatusColor(emp.status)} size="small" />
                          </TableCell>
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

      {/* Floating Action Button */}
      <Fab color="primary" aria-label="add" sx={{ position: 'fixed', bottom: 16, right: 16 }}>
        <AddIcon />
      </Fab>
    </Box>
  );
}
