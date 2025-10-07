import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Dashboard = () => {
  const [backendState, setBackendState] = useState('offline');
  const [dbStats, setDbStats] = useState({
    totalDatasets: 0,
    totalRecords: 0,
    lastGenerated: null
  });

  useEffect(() => {
    // Test backend connection
    const testConnection = async () => {
      try {
        const response = await axios.get('/api/health');
        setBackendState('online');
        setDbStats(response.data.stats || {});
      } catch (error) {
        console.error('Backend connection failed:', error);
        setBackendState('offline');
      }
    };

    testConnection();
    const interval = setInterval(testConnection, 30000); // Check every 30 seconds

    return () => clearInterval(interval);
  }, []); // Fixed: Empty dependency array is correct

  return (
    <div className="dashboard">
      <h2>📊 Overview</h2>
      
      <div className="grid">
        <div className="card">
          <h3>System Status</h3>
          <p>
            <span className={`status-indicator status-${backendState}`}></span>
            Backend: {backendState === 'online' ? 'Connected' : 'Disconnected'}
          </p>
          <p>Frontend: Online</p>
        </div>

        <div className="card">
          <h3>Database Snapshot</h3>
          <p>Total Datasets: {dbStats.totalDatasets}</p>
          <p>Total Records: {dbStats.totalRecords}</p>
          <p>Last Generated: {dbStats.lastGenerated || 'Never'}</p>
        </div>
      </div>

      <div className="card">
        <h3>Activity Feed</h3>
        <p>Welcome to FinTech DataGen. The FinTech Data Curator is wired in and ready.</p>
        <ul>
          <li>✅ React UI live</li>
          <li>✅ Flask API running</li>
          <li>✅ MongoDB wiring configured</li>
          <li>✅ Curator integration enabled</li>
          <li>✅ CSV/JSON exports available</li>
        </ul>
      </div>
    </div>
  );
};

export default Dashboard;