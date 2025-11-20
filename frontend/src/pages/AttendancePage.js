import React, { useEffect, useState } from 'react';
import { Box, Card, CardContent, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Dialog, DialogTitle, DialogContent, TextField, CircularProgress } from '@mui/material';
import { fetchAttendanceRecords, recordAttendance } from '../services/api';
import AddIcon from '@mui/icons-material/Add';
import { format } from 'date-fns';
import { ar } from 'date-fns/locale';

export default function AttendancePage() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);
  const [formData, setFormData] = useState({ employee_id: '', date: '', status: 'حاضر' });

  useEffect(() => {
    fetchAttendanceRecords()
      .then(data => {
        setRecords(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  const handleAddRecord = async () => {
    try {
      const newRecord = await recordAttendance(formData);
      setRecords([...records, newRecord]);
      setOpen(false);
      setFormData({ employee_id: '', date: '', status: 'حاضر' });
    } catch (err) {
      alert('فشل إضافة السجل: ' + err.message);
    }
  };

  if (loading) return <CircularProgress sx={{ mt: 20 }} />;

  return (
    <Box sx={{ mt: 12, mb: 4 }}>
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
              <TableCell>التاريخ</TableCell>
              <TableCell>الحالة</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {records.map((r) => (
              <TableRow key={r.id}>
                <TableCell>{r.employee_name}</TableCell>
                <TableCell>{format(new Date(r.date), 'dd/MM/yyyy', { locale: ar })}</TableCell>
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

      <Dialog open={open} onClose={() => setOpen(false)}>
        <DialogTitle>إضافة سجل حضور جديد</DialogTitle>
        <DialogContent sx={{ pt: 2 }}>
          <TextField
            fullWidth
            label="معرف الموظف"
            type="number"
            value={formData.employee_id}
            onChange={(e) => setFormData({ ...formData, employee_id: e.target.value })}
            sx={{ mb: 2 }}
          />
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
            SelectProps={{ native: true }}
          >
            <option value="حاضر">حاضر</option>
            <option value="غائب">غائب</option>
            <option value="إجازة">إجازة</option>
          </TextField>
          <Box sx={{ mt: 2, display: 'flex', gap: 1 }}>
            <Button variant="contained" onClick={handleAddRecord} fullWidth>
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