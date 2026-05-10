import React, { useEffect, useState } from 'react';
import {
  Alert,
  CircularProgress,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { fetchEmployees } from '../services/api';

export default function EmployeesPage() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let mounted = true;
    fetchEmployees()
      .then((data) => {
        if (mounted) setRows(data);
      })
      .catch((err) => {
        if (mounted) setError(err.message || 'فشل تحميل الموظفين');
      })
      .finally(() => {
        if (mounted) setLoading(false);
      });
    return () => {
      mounted = false;
    };
  }, []);

  if (loading) return <CircularProgress sx={{ mt: 20 }} />;
  if (error) return <Alert severity="error" sx={{ mt: 20 }}>{error}</Alert>;

  return (
    <div style={{ marginTop: 80 }}>
      <Typography variant="h5" gutterBottom>{t('employees')}</Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>الكود</TableCell>
              <TableCell>الاسم</TableCell>
              <TableCell>الوظيفة</TableCell>
              <TableCell>الموقع</TableCell>
              <TableCell>مركز التكلفة</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {rows.map((r) => (
              <TableRow
                key={r.id}
                hover
                onClick={() => navigate(`/employees/${r.id}`)}
                sx={{ cursor: 'pointer' }}
              >
                <TableCell>{r.code}</TableCell>
                <TableCell>{r.name}</TableCell>
                <TableCell>{r.role}</TableCell>
                <TableCell>{r.site}</TableCell>
                <TableCell>{r.costCenter}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
}
