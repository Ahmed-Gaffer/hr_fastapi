import React, { useEffect, useState } from 'react';
import { Box, Card, CardContent, Typography, Grid, CircularProgress, Select, MenuItem, FormControl, InputLabel } from '@mui/material';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { fetchSalaryReports, fetchAttendanceStats } from '../services/api';

const COLORS = ['#0B75BF', '#F59E0B', '#10B981', '#EF4444'];

export default function ReportsPage() {
  const [salaryData, setSalaryData] = useState([]);
  const [attendanceData, setAttendanceData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [reportType, setReportType] = useState('salary');

  useEffect(() => {
    Promise.all([fetchSalaryReports(), fetchAttendanceStats()])
      .then(([salary, attendance]) => {
        setSalaryData(salary);
        setAttendanceData(attendance);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) return <CircularProgress sx={{ mt: 20 }} />;

  return (
    <Box sx={{ mt: 12, mb: 4 }}>
      <Box sx={{ mb: 3, display: 'flex', gap: 2, alignItems: 'center' }}>
        <Typography variant="h5">التقارير والإحصائيات</Typography>
        <FormControl sx={{ minWidth: 200 }}>
          <InputLabel>نوع التقرير</InputLabel>
          <Select value={reportType} onChange={(e) => setReportType(e.target.value)} label="نوع التقرير">
            <MenuItem value="salary">الرواتب</MenuItem>
            <MenuItem value="attendance">الحضور</MenuItem>
            <MenuItem value="both">الكل</MenuItem>
          </Select>
        </FormControl>
      </Box>

      <Grid container spacing={3}>
        {(reportType === 'salary' || reportType === 'both') && (
          <Grid item xs={12} lg={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>تطور الرواتب الشهرية</Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={salaryData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="total" stroke="#0B75BF" name="الإجمالي" />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>
        )}

        {(reportType === 'attendance' || reportType === 'both') && (
          <Grid item xs={12} lg={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>إحصائيات الحضور</Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie data={attendanceData} cx="50%" cy="50%" labelLine={false} label dataKey="value">
                      {attendanceData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>
        )}

        {(reportType === 'salary' || reportType === 'both') && (
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>توزيع الرواتب حسب الأقسام</Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={salaryData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="department" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="total" fill="#F59E0B" name="الإجمالي" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>
        )}
      </Grid>
    </Box>
  );
}