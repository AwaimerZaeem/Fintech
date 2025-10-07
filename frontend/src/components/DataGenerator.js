import React, { useState } from 'react';
import axios from 'axios';

const DataGenerator = () => {
  const [generatorForm, setGeneratorForm] = useState({
    symbol: 'AAPL',
    exchange: 'NASDAQ',
    days: '7'
  });
  const [isGenerating, setIsGenerating] = useState(false);
  const [genOutcome, setGenOutcome] = useState(null);
  const [genPayload, setGenPayload] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setGeneratorForm(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsGenerating(true);
    setResult(null);
    setGeneratedData(null);

    try {
      // Convert days to integer
      const daysInt = parseInt(generatorForm.days);
      if (isNaN(daysInt) || daysInt < 1) {
        throw new Error('Days must be a positive number');
      }

      const response = await axios.post('/api/generate', {
        symbol: generatorForm.symbol,
        exchange: generatorForm.exchange,
        days: daysInt,
        dataType: 'financial'
      });
      
      setGenOutcome({
        success: true,
        data: response.data
      });
      
      setGenPayload(response.data);
      
    } catch (error) {
      setGenOutcome({
        success: false,
        error: error.response?.data?.error || error.message || 'Failed to generate data'
      });
    } finally {
      setIsGenerating(false);
    }
  };

  const downloadCSV = async () => {
    if (!genPayload) return;
    
    try {
      const response = await axios.get(`/api/datasets/${genPayload.dataset_id}/csv`, {
        responseType: 'blob'
      });
      const blob = new Blob([response.data], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${generatorForm.symbol}_${generatorForm.exchange}_data.csv`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Error downloading CSV:', error);
      alert('Error downloading CSV file');
    }
  };

  const downloadJSON = async () => {
    if (!genPayload) return;
    
    try {
      const response = await axios.get(`/api/datasets/${genPayload.dataset_id}/json`);
      const blob = new Blob([JSON.stringify(response.data, null, 2)], { type: 'application/json' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${generatorForm.symbol}_${generatorForm.exchange}_data.json`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Error downloading JSON:', error);
      alert('Error downloading JSON file');
    }
  };

  return (
    <div className="data-generator">
      <h2>🔧 Data Builder</h2>
      
      <div className="card">
        <h3>Create a Financial Dataset</h3>
        <p>Provide a symbol, exchange, and time window to curate data via the integrated FinTech Data Curator.</p>
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="symbol">Symbol or Ticker</label>
            <input
              type="text"
              id="symbol"
              name="symbol"
              value={generatorForm.symbol}
              onChange={handleInputChange}
              placeholder="e.g., AAPL, BTC-USD, TSLA, MSFT"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="exchange">Exchange</label>
            <input
              type="text"
              id="exchange"
              name="exchange"
              value={generatorForm.exchange}
              onChange={handleInputChange}
              placeholder="e.g., NASDAQ, NYSE, Crypto, BSE"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="days">Days of History</label>
            <input
              type="text"
              id="days"
              name="days"
              value={generatorForm.days}
              onChange={handleInputChange}
              placeholder="e.g., 7, 30, 90"
              required
            />
          </div>

          <button 
            type="submit" 
            className="btn"
            disabled={isGenerating}
          >
            {isGenerating ? 'Generating…' : 'Generate Dataset'}
          </button>
        </form>
      </div>

      {genOutcome && (
        <div className="card">
          <h3>Generation Result</h3>
          {genOutcome.success ? (
            <div>
              <p className="success-message">✅ Dataset generated successfully!</p>
              <div className="data-summary">
                <p><strong>Symbol:</strong> {genOutcome.data.symbol}</p>
                <p><strong>Exchange:</strong> {genOutcome.data.exchange}</p>
                <p><strong>Records Generated:</strong> {genOutcome.data.records_count}</p>
                <p><strong>Days Requested:</strong> {genOutcome.data.days}</p>
                <p><strong>Dataset ID:</strong> {genOutcome.data.dataset_id}</p>
              </div>
              
              <div>
                <h4>Download</h4>
                <div className="download-buttons">
                  <button 
                    className="btn" 
                    onClick={downloadCSV}
                    style={{ backgroundColor: '#28a745' }}
                  >
                    📊 Download CSV
                  </button>
                  <button 
                    className="btn" 
                    onClick={downloadJSON}
                    style={{ backgroundColor: '#17a2b8' }}
                  >
                    📄 Download JSON
                  </button>
                </div>
              </div>
            </div>
          ) : (
            <div>
              <p className="error-message">❌ Error: {genOutcome.error}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default DataGenerator;