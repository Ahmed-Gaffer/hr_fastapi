import React from 'react';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import MenuIcon from '@mui/icons-material/Menu';
import ExitToAppIcon from '@mui/icons-material/ExitToApp';
import { useTranslation } from 'react-i18next';

export default function TopBar({ open, setOpen }) {
  const { t } = useTranslation();
  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.href = '/login';
  };
  return (
    <AppBar position="fixed" color="inherit" elevation={1} sx={{ zIndex: theme => theme.zIndex.drawer + 1 }}>
      <Toolbar>
        <IconButton edge="end" color="inherit" onClick={() => setOpen(!open)} aria-label="menu">
          <MenuIcon />
        </IconButton>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1, textAlign: 'center' }}>
          {t('appTitle')}
        </Typography>
        <IconButton color="inherit" onClick={handleLogout} aria-label="logout">
          <ExitToAppIcon />
        </IconButton>
      </Toolbar>
    </AppBar>
  );
}