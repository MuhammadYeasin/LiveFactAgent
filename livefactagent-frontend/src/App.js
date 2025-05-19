import React, { useState, useEffect, useRef } from 'react';
import './App.css';

function App() {
  const [isConnected, setIsConnected] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [factCheckResults, setFactCheckResults] = useState([]);
  const [error, setError] = useState('');
  const [manualClaim, setManualClaim] = useState('');
  
  const wsRef = useRef(null);

  // Function to connect to WebSocket
  const connectWebSocket = () => {
    try {
      wsRef.current = new WebSocket('ws://localhost:8000/ws/audio');
      
      wsRef.current.onopen = () => {
        console.log('WebSocket connected!');
        setIsConnected(true);
        setError('');
      };
      
      wsRef.current.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        if (data.transcript) {
          setTranscript(data.transcript);
        }
        
        if (data.results) {
          setFactCheckResults(data.results);
        }
        
        if (data.error) {
          setError(data.error);
        }
      };
      
      wsRef.current.onerror = (error) => {
        console.error('WebSocket error:', error);
        setError('WebSocket error: Cannot connect to the server. Make sure the FastAPI backend is running on port 8000.');
        setIsConnected(false);
      };
      
      wsRef.current.onclose = () => {
        console.log('WebSocket closed');
        setIsConnected(false);
      };
    } catch (err) {
      console.error('Error creating WebSocket:', err);
      setError('Error creating WebSocket connection: ' + err.message);
    }
  };

  // Function to disconnect WebSocket
  const disconnectWebSocket = () => {
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
  };

  // Toggle listening
  const toggleListening = () => {
    if (!isListening) {
      if (!isConnected) {
        connectWebSocket();
      }
      setIsListening(true);
    } else {
      setIsListening(false);
      setTranscript('');
      setFactCheckResults([]);
    }
  };

  // Handle manual claim submission
  const handleManualSubmit = async (e) => {
    e.preventDefault();
    if (!manualClaim.trim()) return;
    
    try {
      const response = await fetch('http://localhost:8000/fact-check', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ claim: manualClaim }),
      });
      
      if (response.ok) {
        const result = await response.json();
        setFactCheckResults([result]);
      } else {
        setError('Error checking claim');
      }
    } catch (err) {
      setError('Network error: ' + err.message);
    }
  };

  // Clean up on unmount
  useEffect(() => {
    return () => {
      disconnectWebSocket();
    };
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>LiveFactAgent: Real-Time Speech Fact-Checker</h1>
      </header>
      
      <main className="App-main">
        <section className="connection-section">
          <h2>Microphone Connection</h2>
          <div className="status">
            Connection Status: 
            <span className={isConnected ? "connected" : "disconnected"}>
              {isConnected ? "Connected" : "Disconnected"}
            </span>
          </div>
          
          <button 
            onClick={toggleListening}
            className={isListening ? "stop-btn" : "start-btn"}
          >
            {isListening ? "Stop Listening" : "Start Listening"}
          </button>
          
          {error && <div className="error">{error}</div>}
        </section>
        
        <section className="manual-check-section">
          <h2>Manual Fact Check</h2>
          <form onSubmit={handleManualSubmit}>
            <input
              type="text"
              value={manualClaim}
              onChange={(e) => setManualClaim(e.target.value)}
              placeholder="Enter a claim to fact check..."
            />
            <button type="submit">Check Claim</button>
          </form>
        </section>
        
        {transcript && (
          <section className="transcript-section">
            <h2>Transcript</h2>
            <p>{transcript}</p>
          </section>
        )}
        
        {factCheckResults.length > 0 && (
          <section className="results-section">
            <h2>Fact Check Results</h2>
            {factCheckResults.map((result, index) => (
              <div className="result-card" key={index}>
                <h3>Claim</h3>
                <p>{result.claim}</p>
                
                <h3>Status</h3>
                <p className={`status-${result.status}`}>
                  {result.status === 'true' ? 'True' : 
                   result.status === 'false' ? 'False' : 'Uncertain'}
                </p>
                
                {result.citations && result.citations.length > 0 && (
                  <>
                    <h3>Citations</h3>
                    <ul className="citations-list">
                      {result.citations.map((citation, i) => (
                        <li key={i}>
                          {citation.text}
                          {citation.url && (
                            <a href={citation.url} target="_blank" rel="noopener noreferrer">
                              {" "}
                              (Source)
                            </a>
                          )}
                        </li>
                      ))}
                    </ul>
                  </>
                )}
              </div>
            ))}
          </section>
        )}
      </main>
    </div>
  );
}

export default App;