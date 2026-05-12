import React, { useEffect, useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Grid,
  CircularProgress,
  Alert,
  Button,
  Table,
  TableHead,
  TableBody,
  TableCell,
  TableRow,
  Paper,
  TableContainer,
} from '@mui/material';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import {
  fetchPayrollSummary,
  fetchEmployeePerformance,
  fetchDepartmentAnalysis,
  fetchCostCenterAnalysis,
} from '../services/api';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82ca9d'];

export default function AdvancedAnalyticsPage() {
  const [tab, setTab] = useState('payroll');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // فلاتر
  const currentYear = new Date().getFullYear();
  const years = Array.from({ length: currentYear - 2022 + 1 }, (_, index) => 2022 + index);
  const [year, setYear] = useState(currentYear);
  const [month, setMonth] = useState(new Date().getMonth() + 1);

  // البيانات
  const [payrollData, setPayrollData] = useState([]);
  const [departmentData, setDepartmentData] = useState([]);
  const [costCenterData, setCostCenterData] = useState([]);
  const [performanceData, setPerformanceData] = useState([]);

  const loadPayrollSummary = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await fetchPayrollSummary(year, month);
      setPayrollData(data);
    } catch (err) {
      setError('فشل تحميل ملخص الرواتب');
    } finally {
      setLoading(false);
    }
  };

  const loadDepartmentAnalysis = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await fetchDepartmentAnalysis(year, month);
      setDepartmentData(data);
    } catch (err) {
      setError('فشل تحميل تحليل الأقسام');
    } finally {
      setLoading(false);
    }
  };

  const loadCostCenterAnalysis = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await fetchCostCenterAnalysis(year, month);
      setCostCenterData(data);
    } catch (err) {
      setError('فشل تحميل تحليل مراكز التكلفة');
    } finally {
      setLoading(false);
    }
  };

  const loadEmployeePerformance = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await fetchEmployeePerformance(year, month);
      setPerformanceData(data.results || data);
    } catch (err) {
      setError('فشل تحميل أداء الموظفين');
    } finally {
      setLoading(false);
    }
  };

  const handleTabChange = (newTab) => {
    setTab(newTab);
    switch (newTab) {
      case 'payroll':
        loadPayrollSummary();
        break;
      case 'department':
        loadDepartmentAnalysis();
        break;
      case 'cost-center':
        loadCostCenterAnalysis();
        break;
      case 'performance':
        loadEmployeePerformance();
        break;
      default:
        break;
    }
  };

  useEffect(() => {
    switch (tab) {
      case 'payroll':
        loadPayrollSummary();
        break;
      case 'department':
        loadDepartmentAnalysis();
        break;
      case 'cost-center':
        loadCostCenterAnalysis();
        break;
      case 'performance':
        loadEmployeePerformance();
        break;
      default:
        break;
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [tab, year, month]);

  return (
    <Box sx={{ mt: 12, mb: 4 }}>
      <Typography variant="h4" gutterBottom>التقارير والتحليلات المتقدمة</Typography>

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={2}>
            <Grid item xs={12} md={3}>
              <FormControl fullWidth size="small">
                <InputLabel>السنة</InputLabel>
                <Select value={year} label="السنة" onChange={(e) => setYear(e.target.value)}>
                  {years.map((y) => (
                    <MenuItem key={y} value={y}>{y}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={3}>
              <FormControl fullWidth size="small">
                <InputLabel>الشهر</InputLabel>
                <Select value={month} label="الشهر" onChange={(e) => setMonth(e.target.value)}>
                  {Array.from({ length: 12 }, (_, i) => (
                    <MenuItem key={i + 1} value={i + 1}>
                      {new Date(2024, i).toLocaleDateString('ar-EG', { month: 'long' })}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={6}>
              <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                {[
                  { id: 'payroll', label: 'ملخص الرواتب' },
                  { id: 'department', label: 'الأقسام' },
                  { id: 'cost-center', label: 'مراكز التكلفة' },
                  { id: 'performance', label: 'أداء الموظفين' },
                ].map((tab_item) => (
                  <Button
                    key={tab_item.id}
                    variant={tab === tab_item.id ? 'contained' : 'outlined'}
                    onClick={() => handleTabChange(tab_item.id)}
                    size="small"
                  >
                    {tab_item.label}
                  </Button>
                ))}
              </Box>
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
          {tab === 'payroll' && (
            <Grid container spacing={3}>
              {payrollData.length > 0 && (
                <>
                  <Grid item xs={12} md={6}>
                    <Card>
                      <CardContent>
                        <Typography variant="h6" gutterBottom>توزيع الرواتب</Typography>
                        <ResponsiveContainer width="100%" height={300}>
                          <PieChart>
                            <Pie
                              data={payrollData}
                              dataKey="total_salary"
                              nameKey="month"
                              cx="50%"
                              cy="50%"
                              outerRadius={80}
                              label
                            >
                              {payrollData.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                              ))}
                            </Pie>
                            <Tooltip formatter={(value) => value.toLocaleString()} />
                          </PieChart>
                        </ResponsiveContainer>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <Card>
                      <CardContent>
                        <Typography variant="h6" gutterBottom>إجمالي الرواتب والعدد</Typography>
                        <ResponsiveContainer width="100%" height={300}>
                          <BarChart data={payrollData}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="month" />
                            <YAxis />
                            <Tooltip formatter={(value) => value.toLocaleString()} />
                            <Legend />
                            <Bar dataKey="total_salary" fill="#8884d8" name="إجمالي الراتب" />
                            <Bar dataKey="count" fill="#82ca9d" name="عدد الموظفين" />
                          </BarChart>
                        </ResponsiveContainer>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid item xs={12}>
                    <Card>
                      <CardContent>
                        <Typography variant="h6" gutterBottom>تفاصيل الرواتب</Typography>
                        <TableContainer component={Paper}>
                          <Table size="small">
                            <TableHead>
                              <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
                                <TableCell>الشهر</TableCell>
                                <TableCell align="right">عدد الموظفين</TableCell>
                                <TableCell align="right">إجمالي الراتب</TableCell>
                                <TableCell align="right">متوسط الراتب</TableCell>
                              </TableRow>
                            </TableHead>
                            <TableBody>
                              {payrollData.map((row, idx) => (
                                <TableRow key={idx}>
                                  <TableCell>{row.month}</TableCell>
                                  <TableCell align="right">{row.count}</TableCell>
                                  <TableCell align="right">{row.total_salary?.toLocaleString()}</TableCell>
                                  <TableCell align="right">{row.avg_salary?.toLocaleString()}</TableCell>
                                </TableRow>
                              ))}
                            </TableBody>
                          </Table>
                        </TableContainer>
                      </CardContent>
                    </Card>
                  </Grid>
                </>
              )}
            </Grid>
          )}

          {tab === 'department' && (
            <Grid container spacing={3}>
              {departmentData.length > 0 && (
                <>
                  <Grid item xs={12} md={6}>
                    <Card>
                      <CardContent>
                        <Typography variant="h6" gutterBottom>عدد الموظفين بالقسم</Typography>
                        <ResponsiveContainer width="100%" height={300}>
                          <BarChart data={departmentData} layout="vertical">
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis type="number" />
                            <YAxis dataKey="department" type="category" width={100} />
                            <Tooltip />
                            <Bar dataKey="employee_count" fill="#8884d8" name="عدد الموظفين" />
                          </BarChart>
                        </ResponsiveContainer>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <Card>
                      <CardContent>
                        <Typography variant="h6" gutterBottom>متوسط الراتب بالقسم</Typography>
                        <ResponsiveContainer width="100%" height={300}>
                          <LineChart data={departmentData}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="department" />
                            <YAxis />
                            <Tooltip formatter={(value) => value.toLocaleString()} />
                            <Legend />
                            <Line type="monotone" dataKey="avg_salary" stroke="#82ca9d" name="متوسط الراتب" />
                          </LineChart>
                        </ResponsiveContainer>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid item xs={12}>
                    <Card>
                      <CardContent>
                        <Typography variant="h6" gutterBottom>تفاصيل الأقسام</Typography>
                        <TableContainer component={Paper}>
                          <Table size="small">
                            <TableHead>
                              <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
                                <TableCell>القسم</TableCell>
                                <TableCell align="right">عدد الموظفين</TableCell>
                                <TableCell align="right">إجمالي الراتب</TableCell>
                                <TableCell align="right">متوسط الراتب</TableCell>
                              </TableRow>
                            </TableHead>
                            <TableBody>
                              {departmentData.map((row, idx) => (
                                <TableRow key={idx}>
                                  <TableCell>{row.department}</TableCell>
                                  <TableCell align="right">{row.employee_count}</TableCell>
                                  <TableCell align="right">{row.total_salary?.toLocaleString()}</TableCell>
                                  <TableCell align="right">{row.avg_salary?.toLocaleString()}</TableCell>
                                </TableRow>
                              ))}
                            </TableBody>
                          </Table>
                        </TableContainer>
                      </CardContent>
                    </Card>
                  </Grid>
                </>
              )}
            </Grid>
          )}

          {tab === 'cost-center' && (
            <Grid container spacing={3}>
              {costCenterData.length > 0 && (
                <>
                  <Grid item xs={12} md={6}>
                    <Card>
                      <CardContent>
                        <Typography variant="h6" gutterBottom>عدد الموظفين بمركز التكلفة</Typography>
                        <ResponsiveContainer width="100%" height={300}>
                          <PieChart>
                            <Pie
                              data={costCenterData}
                              dataKey="employee_count"
                              nameKey="cost_center"
                              cx="50%"
                              cy="50%"
                              outerRadius={80}
                              label
                            >
                              {costCenterData.map((entry, index) => (
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
                    <Card>
                      <CardContent>
                        <Typography variant="h6" gutterBottom>إجمالي الراتب بمركز التكلفة</Typography>
                        <ResponsiveContainer width="100%" height={300}>
                          <BarChart data={costCenterData}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="cost_center" />
                            <YAxis />
                            <Tooltip formatter={(value) => value.toLocaleString()} />
                            <Bar dataKey="total_salary" fill="#8884d8" name="إجمالي الراتب" />
                          </BarChart>
                        </ResponsiveContainer>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid item xs={12}>
                    <Card>
                      <CardContent>
                        <Typography variant="h6" gutterBottom>تفاصيل مراكز التكلفة</Typography>
                        <TableContainer component={Paper}>
                          <Table size="small">
                            <TableHead>
                              <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
                                <TableCell>مركز التكلفة</TableCell>
                                <TableCell align="right">عدد الموظفين</TableCell>
                                <TableCell align="right">إجمالي الراتب</TableCell>
                                <TableCell align="right">متوسط الراتب</TableCell>
                              </TableRow>
                            </TableHead>
                            <TableBody>
                              {costCenterData.map((row, idx) => (
                                <TableRow key={idx}>
                                  <TableCell>{row.cost_center}</TableCell>
                                  <TableCell align="right">{row.employee_count}</TableCell>
                                  <TableCell align="right">{row.total_salary?.toLocaleString()}</TableCell>
                                  <TableCell align="right">{row.avg_salary?.toLocaleString()}</TableCell>
                                </TableRow>
                              ))}
                            </TableBody>
                          </Table>
                        </TableContainer>
                      </CardContent>
                    </Card>
                  </Grid>
                </>
              )}
            </Grid>
          )}

          {tab === 'performance' && (
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>أداء الموظفين</Typography>
                <TableContainer component={Paper}>
                  <Table size="small">
                    <TableHead>
                      <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
                        <TableCell>الاسم</TableCell>
                        <TableCell align="right">الحضور</TableCell>
                        <TableCell align="right">الغياب</TableCell>
                        <TableCell align="right">نسبة الحضور %</TableCell>
                        <TableCell align="right">متوسط الراتب</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {performanceData.slice(0, 100).map((row, idx) => (
                        <TableRow key={idx}>
                          <TableCell>{row.employee_name}</TableCell>
                          <TableCell align="right">{row.present_count || 0}</TableCell>
                          <TableCell align="right">{row.absent_count || 0}</TableCell>
                          <TableCell align="right">{row.attendance_rate?.toFixed(2)}%</TableCell>
                          <TableCell align="right">{row.avg_salary?.toLocaleString()}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </CardContent>
            </Card>
          )}
        </>
      )}
    </Box>
  );
}
