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
import AnalyticsIcon from '@mui/icons-material/Analytics';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';
import BusinessIcon from '@mui/icons-material/Business';
import SettingsIcon from '@mui/icons-material/Settings';
import SettingsApplicationsIcon from '@mui/icons-material/SettingsApplications';
import GroupIcon from '@mui/icons-material/Group';
import { Link, useLocation } from 'react-router-dom';

const drawerWidth = 240;

export default function SideBar({ open }) {
  const location = useLocation();
  const menuItems = [
    { label: 'لوحة التحكم', icon: <DashboardIcon />, path: '/' },
    { label: 'الموظفين', icon: <PeopleIcon />, path: '/employees' },
    { label: 'الحضور', icon: <EventNoteIcon />, path: '/attendance' },
    { label: 'الرواتب', icon: <AttachMoneyIcon />, path: '/salary' },
    { label: 'مكونات الراتب', icon: <AttachMoneyIcon />, path: '/salary-components' },
    { label: 'المواقع', icon: <BusinessIcon />, path: '/site' },
    { label: 'التقارير', icon: <AssignmentIcon />, path: '/reports' },
    { label: 'التحليلات', icon: <AnalyticsIcon />, path: '/analytics' },
    { label: 'النظام', icon: <SettingsIcon />, path: '/system' },
    { label: 'الإعدادات', icon: <SettingsApplicationsIcon />, path: '/settings' },
    { label: 'المستأجرين', icon: <GroupIcon />, path: '/tenants' },
    { label: 'استيراد', icon: <FileUploadIcon />, path: '/import' }
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