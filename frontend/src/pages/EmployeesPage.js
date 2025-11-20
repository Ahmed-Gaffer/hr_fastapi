import React, { useEffect, useState } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography } from '@mui/material';
import { fetchEmployees } from '../services/api';
import { useTranslation } from 'react-i18next';

export default function EmployeesPage() {
  const { t } = useTranslation();
  const [rows, setRows] = useState([]);

  useEffect(() => {
    let mounted = true;
    fetchEmployees().then(data => {
      if (mounted) setRows(data);
    });
    return () => { mounted = false; };
  }, []);

  return (
    <div style={{ marginTop: 80 }}>
      <Typography variant="h5" gutterBottom>{t('employees')}</Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>الاسم</TableCell>
              <TableCell>المنصب</TableCell>
              <TableCell>الموقع</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {rows.map((r) => (
              <TableRow key={r.id}>
                <TableCell>{r.name}</TableCell>
                <TableCell>{r.role}</TableCell>
                <TableCell>{r.site}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
}
