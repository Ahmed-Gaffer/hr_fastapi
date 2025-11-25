import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Alert,
  CircularProgress,
  LinearProgress
} from '@mui/material';
import { useDropzone } from 'react-dropzone';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import { importEmployeesFromExcel } from '../services/api';

export default function ImportPage() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState('');
  const [error, setError] = useState('');
  const [progress, setProgress] = useState(0);

  const { getRootProps, getInputProps } = useDropzone({
    accept: { 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'] },
    onDrop: (files) => {
      if (files.length > 0) {
        setFile(files[0]);
        setError('');
        setSuccess('');
      }
    }
  });

  const handleImport = async () => {
    if (!file) {
      setError('اختر ملف Excel أولاً');
      return;
    }
    setLoading(true);
    setProgress(0);

    try {
      const interval = setInterval(() => {
        setProgress((prev) => (prev < 90 ? prev + 10 : prev));
      }, 300);

      const result = await importEmployeesFromExcel(file, false); // false = تجربة (dry-run)
      clearInterval(interval);
      setProgress(100);

      setSuccess(`تم استيراد ${result.count || 0} موظف بنجاح`);
      setFile(null);
      setTimeout(() => setProgress(0), 1000);
    } catch (err) {
      const errorMsg =
        err.response?.data?.detail ||
        err.response?.data?.error ||
        err.message ||
        "فشل الاستيراد";

      setError(`خطأ في الاستيراد: ${errorMsg}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ mt: 12, mb: 4, maxWidth: 600, mx: 'auto' }}>
      <Card>
        <CardContent>
          <Typography variant="h5" gutterBottom>
            استيراد الموظفين من Excel
          </Typography>

          <Box
            {...getRootProps()}
            sx={{
              border: '2px dashed',
              borderColor: file ? 'primary.main' : 'grey.300',
              borderRadius: 2,
              p: 3,
              textAlign: 'center',
              cursor: 'pointer',
              backgroundColor: file ? 'primary.light' : 'grey.50',
              transition: 'all 0.3s',
              '&:hover': {
                borderColor: 'primary.main',
                backgroundColor: 'primary.light'
              }
            }}
          >
            <input {...getInputProps()} />
            <FileUploadIcon sx={{ fontSize: 48, color: 'primary.main', mb: 1 }} />
            <Typography variant="body1">
              اسحب ملف Excel هنا أو انقر للاختيار
            </Typography>
            {file && (
              <Typography variant="body2" color="success.main" sx={{ mt: 1 }}>
                ✓ {file.name}
              </Typography>
            )}
          </Box>

          {progress > 0 && (
            <LinearProgress variant="determinate" value={progress} sx={{ mt: 2 }} />
          )}

          {error && (
            <Alert severity="error" sx={{ mt: 2 }}>
              {error}
            </Alert>
          )}
          {success && (
            <Alert severity="success" sx={{ mt: 2 }}>
              {success}
            </Alert>
          )}

          <Button
            variant="contained"
            fullWidth
            onClick={handleImport}
            disabled={!file || loading}
            sx={{ mt: 2 }}
          >
            {loading ? <CircularProgress size={24} /> : 'استيراد'}
          </Button>
        </CardContent>
      </Card>
    </Box>
  );
}
