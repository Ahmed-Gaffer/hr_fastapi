import React, { useState } from 'react';
import { TextField, Button, Box, Typography, Alert } from '@mui/material';
import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || "http://192.168.10.92:8000/api";

export default function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);
      const res = await axios.post(`${API_BASE}/auth/login`, formData);
      // The response is HTML, extract the token
      const html = res.data;
      const tokenMatch = html.match(/توكن الدخول: <br><code>(.*?)<\/code>/);
      if (tokenMatch) {
        const token = tokenMatch[1];
        localStorage.setItem('token', token);
        window.location.href = '/'; // Redirect to dashboard
      } else {
        setError('فشل في استخراج التوكن');
      }
    } catch (err) {
      setError('بيانات الدخول غير صحيحة');
    }
    setLoading(false);
  };

  return (
    <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
      <Box component="form" onSubmit={handleLogin} sx={{ width: 300 }}>
        <Typography variant="h4" gutterBottom>تسجيل الدخول</Typography>
        {error && <Alert severity="error">{error}</Alert>}
        <TextField
          label="اسم المستخدم"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          fullWidth
          margin="normal"
          required
        />
        <TextField
          label="كلمة المرور"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          fullWidth
          margin="normal"
          required
        />
        <Button type="submit" variant="contained" fullWidth disabled={loading}>
          {loading ? 'جاري...' : 'دخول'}
        </Button>
      </Box>
    </Box>
  );
}