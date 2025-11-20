import React from 'react';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import PeopleIcon from '@mui/icons-material/People';
import DashboardIcon from '@mui/icons-material/Dashboard';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import EventNoteIcon from '@mui/icons-material/EventNote';
import AssignmentIcon from '@mui/icons-material/Assignment';
import { Link, useLocation } from 'react-router-dom';

const drawerWidth = 240;

export default function SideBar({ open }) {
  const location = useLocation();
  const menuItems = [
    { label: 'لوحة التحكم', icon: <DashboardIcon />, path: '/' },
    { label: 'الموظفين', icon: <PeopleIcon />, path: '/employees' },
    { label: 'الحضور', icon: <EventNoteIcon />, path: '/attendance' },
    { label: 'استيراد', icon: <FileUploadIcon />, path: '/import' },
    { label: 'التقارير', icon: <AssignmentIcon />, path: '/reports' }
  ];

  return (
    <Drawer
      variant="permanent"
      anchor="right"
      open={open}
      PaperProps={{ sx: { width: open ? drawerWidth : 72, transition: 'width .2s', mt: 8 } }}
    >
      <List>
        {menuItems.map((item) => (
          <ListItemButton
            key={item.path}
            component={Link}
            to={item.path}
            selected={location.pathname === item.path}
            sx={{ justifyContent: 'flex-end', px: 2 }}
          >
            <ListItemIcon sx={{ minWidth: 0, ml: 2 }}>{item.icon}</ListItemIcon>
            {open && <ListItemText primary={item.label} />}
          </ListItemButton>
        ))}
      </List>
    </Drawer>
  );
}