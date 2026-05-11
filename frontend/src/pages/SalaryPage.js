import React, { useState, useEffect } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Dialog, DialogTitle, DialogContent, DialogActions, TextField } from '@mui/material';
import { fetchSalaries, createSalary } from '../services/api';

export default function SalaryPage() {
  const [salaries, setSalaries] = useState([]);
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({ employee_id: '', amount: '', month: '', year: '' });

  useEffect(() => {
    loadSalaries();
  }, []);

  const loadSalaries = async () => {
    try {
      const data = await fetchSalaries();
      setSalaries(data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleCreate = async () => {
    try {
      await createSalary(form);
      setOpen(false);
      setForm({ employee_id: '', amount: '', month: '', year: '' });
      loadSalaries();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <h1>الرواتب</h1>
      <Button variant="contained" onClick={() => setOpen(true)}>إضافة راتب</Button>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>الموظف</TableCell>
              <TableCell>المبلغ</TableCell>
              <TableCell>الشهر</TableCell>
              <TableCell>السنة</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {salaries.map((s) => (
              <TableRow key={s.id}>
                <TableCell>{s.employee_id}</TableCell>
                <TableCell>{s.amount}</TableCell>
                <TableCell>{s.month}</TableCell>
                <TableCell>{s.year}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <Dialog open={open} onClose={() => setOpen(false)}>
        <DialogTitle>إضافة راتب</DialogTitle>
        <DialogContent>
          <TextField label="معرف الموظف" value={form.employee_id} onChange={(e) => setForm({...form, employee_id: e.target.value})} fullWidth margin="normal" />
          <TextField label="المبلغ" value={form.amount} onChange={(e) => setForm({...form, amount: e.target.value})} fullWidth margin="normal" />
          <TextField label="الشهر" value={form.month} onChange={(e) => setForm({...form, month: e.target.value})} fullWidth margin="normal" />
          <TextField label="السنة" value={form.year} onChange={(e) => setForm({...form, year: e.target.value})} fullWidth margin="normal" />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>إلغاء</Button>
          <Button onClick={handleCreate}>إضافة</Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}