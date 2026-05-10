import React, { useEffect, useState } from 'react';
import {
  Alert,
  Box,
  Button,
  CircularProgress,
  Dialog,
  DialogContent,
  DialogTitle,
  MenuItem,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import { createAttendance, fetchAttendances, fetchEmployees } from '../services/api';

export default function AttendancePage() {
  const [records, setRecords] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [open, setOpen] = useState(false);
  const [formData, setFormData] = useState({ employee_id: '', date: '', status: 'حاضر' });

  useEffect(() => {
    Promise.all([fetchAttendances(), fetchEmployees()])
      .then(([attendanceRows, employeeRows]) => {
        setRecords(attendanceRows);
        setEmployees(employeeRows);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message || 'فشل تحميل الحضور');
        setLoading(false);
      });
  }, []);

  const handleAdd = async () => {
    try {
      const newRecord = await createAttendance(formData);
      setRecords((current) => [...current, newRecord]);
      setOpen(false);
      setFormData({ employee_id: '', date: '', status: 'حاضر' });
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) return <CircularProgress sx={{ mt: 20 }} />;

  return (
    <Box sx={{ mt: 12, mb: 4 }}>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h5">سجل الحضور</Typography>
        <Button variant="contained" startIcon={<AddIcon />} onClick={() => setOpen(true)}>
          إضافة سجل
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
              <TableCell>الموظف</TableCell>
              <TableCell>الموقع</TableCell>
              <TableCell>التاريخ</TableCell>
              <TableCell>الحالة</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {records.map((r) => (
              <TableRow key={r.id}>
                <TableCell>{r.employee_name}</TableCell>
                <TableCell>{r.site_name}</TableCell>
                <TableCell>{r.date}</TableCell>
                <TableCell>
                  <Typography sx={{ color: r.status === 'حاضر' ? 'green' : 'red' }}>
                    {r.status}
                  </Typography>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={open} onClose={() => setOpen(false)} fullWidth maxWidth="sm">
        <DialogTitle>إضافة سجل حضور جديد</DialogTitle>
        <DialogContent sx={{ pt: 2 }}>
          <TextField
            fullWidth
            select
            label="الموظف"
            value={formData.employee_id}
            onChange={(e) => setFormData({ ...formData, employee_id: e.target.value })}
            sx={{ mb: 2, mt: 1 }}
          >
            {employees.map((employee) => (
              <MenuItem key={employee.id} value={employee.id}>
                {employee.code} - {employee.name}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            fullWidth
            label="التاريخ"
            type="date"
            value={formData.date}
            onChange={(e) => setFormData({ ...formData, date: e.target.value })}
            InputLabelProps={{ shrink: true }}
            sx={{ mb: 2 }}
          />
          <TextField
            fullWidth
            select
            label="الحالة"
            value={formData.status}
            onChange={(e) => setFormData({ ...formData, status: e.target.value })}
            sx={{ mb: 2 }}
          >
            <MenuItem value="حاضر">حاضر</MenuItem>
            <MenuItem value="غائب">غائب</MenuItem>
            <MenuItem value="إجازة">إجازة</MenuItem>
          </TextField>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <Button variant="contained" onClick={handleAdd} fullWidth disabled={!formData.employee_id || !formData.date}>
              حفظ
            </Button>
            <Button variant="outlined" onClick={() => setOpen(false)} fullWidth>
              إلغاء
            </Button>
          </Box>
        </DialogContent>
      </Dialog>
    </Box>
  );
}
