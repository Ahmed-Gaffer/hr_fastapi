import React, { useEffect, useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  CircularProgress,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Alert,
  Table,
  TableHead,
  TableBody,
  TableCell,
  TableRow,
  Button,
  Stack,
} from '@mui/material';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import {
  fetchSalaryReports,
  fetchSalaryByDepartment,
  fetchSalaryByCostCenter,
  fetchSalaryBySite,
  fetchAttendanceStats,
  fetchAttendanceBySite,
  fetchAttendanceByCostCenter,
  fetchEmployeesByDepartment,
  fetchEmployeesBySite,
  fetchEmployeesByCostCenter,
  fetchEmployeesByJobTitle,
  fetchEmployeesWithoutDepartment,
  fetchOvertimeSummary,
} from '../services/api';

const COLORS = ['#0B75BF', '#F59E0B', '#10B981', '#EF4444', '#8B5CF6', '#14B8A6'];

const reportOptions = [
  { value: 'salary', label: 'تقرير الرواتب الشهري' },
  { value: 'salary-department', label: 'الرواتب حسب القسم' },
  { value: 'salary-cost-center', label: 'الرواتب حسب مركز التكلفة' },
  { value: 'salary-site', label: 'الرواتب حسب الموقع' },
  { value: 'attendance', label: 'الحضور حسب الحالة' },
  { value: 'attendance-site', label: 'الحضور حسب الموقع' },
  { value: 'attendance-cost-center', label: 'الحضور حسب مركز التكلفة' },
  { value: 'employees-department', label: 'عدد الموظفين حسب القسم' },
  { value: 'employees-site', label: 'عدد الموظفين حسب الموقع' },
  { value: 'employees-cost-center', label: 'عدد الموظفين حسب مركز التكلفة' },
  { value: 'employees-job-title', label: 'عدد الموظفين حسب المسمى الوظيفي' },
  { value: 'employees-without-department', label: 'الموظفين بدون قسم' },
  { value: 'overtime', label: 'ساعات العمل الإضافية' },
];

const chartTypes = [
  { value: 'line', label: 'خطّي' },
  { value: 'bar', label: 'عمودي' },
  { value: 'pie', label: 'دائري' },
  { value: 'table', label: 'جدول' },
];

const getTitle = (type) => {
  switch (type) {
    case 'salary':
      return 'تطور الرواتب الشهرية';
    case 'salary-department':
      return 'رواتب حسب القسم';
    case 'salary-cost-center':
      return 'رواتب حسب مركز التكلفة';
    case 'salary-site':
      return 'رواتب حسب الموقع';
    case 'attendance':
      return 'الحضور حسب الحالة';
    case 'attendance-site':
      return 'الحضور حسب الموقع';
    case 'attendance-cost-center':
      return 'الحضور حسب مركز التكلفة';
    case 'employees-department':
      return 'عدد الموظفين حسب القسم';
    case 'employees-site':
      return 'عدد الموظفين حسب الموقع';
    case 'employees-cost-center':
      return 'عدد الموظفين حسب مركز التكلفة';
    case 'employees-job-title':
      return 'عدد الموظفين حسب المسمى الوظيفي';
    case 'employees-without-department':
      return 'الموظفين بدون قسم';
    case 'overtime':
      return 'عمل إضافي شهري';
    default:
      return 'التقارير';
  }
};

export default function ReportsPage() {
  const [reportType, setReportType] = useState('salary');
  const [chartType, setChartType] = useState('bar');
  const [data, setData] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const loadReport = async (type) => {
    setLoading(true);
    setError('');
    try {
      let result = [];
      let summaryResult = null;

      switch (type) {
        case 'salary':
          result = await fetchSalaryReports();
          summaryResult = { label: 'إجمالي الرواتب', value: result.reduce((sum, row) => sum + Number(row.total || 0), 0) };
          break;
        case 'salary-department':
          result = await fetchSalaryByDepartment();
          break;
        case 'salary-cost-center':
          result = await fetchSalaryByCostCenter();
          break;
        case 'salary-site':
          result = await fetchSalaryBySite();
          break;
        case 'attendance':
          result = await fetchAttendanceStats();
          summaryResult = { label: 'نسبة الحضور', value: `${result.percent_present || 0}%` };
          result = result.stats || [];
          break;
        case 'attendance-site':
          result = await fetchAttendanceBySite();
          break;
        case 'attendance-cost-center':
          result = await fetchAttendanceByCostCenter();
          break;
        case 'employees-department':
          result = await fetchEmployeesByDepartment();
          summaryResult = { label: 'إجمالي الموظفين', value: result.reduce((sum, row) => sum + Number(row.value || 0), 0) };
          break;
        case 'employees-site':
          result = await fetchEmployeesBySite();
          summaryResult = { label: 'إجمالي الموظفين', value: result.reduce((sum, row) => sum + Number(row.value || 0), 0) };
          break;
        case 'employees-cost-center':
          result = await fetchEmployeesByCostCenter();
          summaryResult = { label: 'إجمالي الموظفين', value: result.reduce((sum, row) => sum + Number(row.value || 0), 0) };
          break;
        case 'employees-job-title':
          result = await fetchEmployeesByJobTitle();
          summaryResult = { label: 'إجمالي الموظفين', value: result.reduce((sum, row) => sum + Number(row.value || 0), 0) };
          break;
        case 'employees-without-department':
          result = await fetchEmployeesWithoutDepartment();
          summaryResult = { label: 'عدد الموظفين', value: result.reduce((sum, row) => sum + Number(row.value || 0), 0) };
          break;
        case 'overtime':
          result = await fetchOvertimeSummary();
          break;
        default:
          result = [];
      }

      setData(result);
      setSummary(summaryResult);
    } catch (err) {
      setError(err.message || 'فشل تحميل التقرير');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadReport(reportType);
  }, [reportType]);

  const renderChart = () => {
    if (!data || data.length === 0) {
      return <Typography>لا توجد بيانات لعرضها في هذا التقرير.</Typography>;
    }

    const dataKey = 'value';
    const labelKey = data[0]?.month ? 'month' : 'name';

    if (chartType === 'table') {
      return (
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>البند</TableCell>
              <TableCell>القيمة</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.map((row, index) => (
              <TableRow key={index}>
                <TableCell>{row[labelKey]}</TableCell>
                <TableCell>{row[dataKey]?.toLocaleString?.() ?? row[dataKey]}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      );
    }

    if (chartType === 'pie') {
      return (
        <ResponsiveContainer width="100%" height={350}>
          <PieChart>
            <Pie data={data} dataKey={dataKey} nameKey={labelKey} cx="50%" cy="50%" outerRadius={120} label>
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      );
    }

    if (chartType === 'line') {
      return (
        <ResponsiveContainer width="100%" height={350}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey={labelKey} />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey={dataKey} stroke="#0B75BF" />
          </LineChart>
        </ResponsiveContainer>
      );
    }

    return (
      <ResponsiveContainer width="100%" height={350}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={labelKey} />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey={dataKey} fill="#0B75BF" />
        </BarChart>
      </ResponsiveContainer>
    );
  };

  return (
    <Box sx={{ mt: 12, mb: 4 }}>
      <Typography variant="h4" gutterBottom>التقارير المرنة</Typography>

      <Grid container spacing={2} alignItems="center">
        <Grid item xs={12} md={5}>
          <FormControl fullWidth>
            <InputLabel>نوع التقرير</InputLabel>
            <Select value={reportType} label="نوع التقرير" onChange={(e) => setReportType(e.target.value)}>
              {reportOptions.map((option) => (
                <MenuItem key={option.value} value={option.value}>
                  {option.label}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={12} md={5}>
          <FormControl fullWidth>
            <InputLabel>شكل العرض</InputLabel>
            <Select value={chartType} label="شكل العرض" onChange={(e) => setChartType(e.target.value)}>
              {chartTypes.map((option) => (
                <MenuItem key={option.value} value={option.value}>
                  {option.label}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={12} md={2}>
          <Button fullWidth variant="contained" onClick={() => loadReport(reportType)}>
            تحديث
          </Button>
        </Grid>
      </Grid>

      {loading ? (
        <CircularProgress sx={{ mt: 4 }} />
      ) : error ? (
        <Alert severity="error" sx={{ mt: 4 }}>{error}</Alert>
      ) : (
        <Box sx={{ mt: 4 }}>
          {summary && (
            <Card sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="subtitle1">{summary.label}</Typography>
                <Typography variant="h5">{summary.value?.toLocaleString ? summary.value.toLocaleString() : summary.value}</Typography>
              </CardContent>
            </Card>
          )}

          <Card>
            <CardContent>
              <Stack direction="row" alignItems="center" justifyContent="space-between" sx={{ mb: 2 }}>
                <Typography variant="h6">{getTitle(reportType)}</Typography>
                <Typography color="text.secondary">عدد الصفوف: {data.length}</Typography>
              </Stack>
              {renderChart()}
            </CardContent>
          </Card>
        </Box>
      )}
    </Box>
  );
}
