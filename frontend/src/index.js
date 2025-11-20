import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';
import './i18n';
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';
import { CacheProvider } from '@emotion/react';
import createCache from '@emotion/cache';
import stylisPluginRtl from 'stylis-plugin-rtl';

const cacheRtl = createCache({
  key: 'muirtl',
  stylisPlugins: [stylisPluginRtl],
});

const theme = createTheme({
  direction: 'rtl',
  typography: {
    fontFamily: ['"Cairo"', 'Noto Sans Arabic', 'Helvetica', 'Arial', 'sans-serif'].join(','),
  },
  palette: {
    primary: { main: '#0B75BF' },
    secondary: { main: '#F59E0B' },
  },
});

document.documentElement.lang = 'ar';
document.documentElement.dir = 'rtl';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <CacheProvider value={cacheRtl}>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <App />
    </ThemeProvider>
  </CacheProvider>
);
