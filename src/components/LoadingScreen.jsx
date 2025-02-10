import React, { useEffect, useState } from 'react';
import './LoadingScreen.css';

const LoadingScreen = ({ businessName }) => {
  const [voltage, setVoltage] = useState(0);
  const [wireProgress, setWireProgress] = useState(0);

  useEffect(() => {
    const voltageInterval = setInterval(() => {
      setVoltage(prev => (prev >= 230 ? 230 : prev + 23));
    }, 300);

    const wireInterval = setInterval(() => {
      setWireProgress(prev => (prev >= 100 ? 0 : prev + 10));
    }, 500);

    return () => {
      clearInterval(voltageInterval);
      clearInterval(wireInterval);
    };
  }, []);

  return (
    <div className="electrician-container">
      {/* Blueprint Background */}
      <div className="blueprint-grid" />

      {/* Animated Circuit Path */}
      <div className="wiring-diagram">
        <div className="circuit-path">
          <div 
            className="live-wire"
            style={{ width: `${wireProgress}%` }}
          />
        </div>
        <div className="connection-dots">
          {[0, 25, 50, 75, 100].map(pos => (
            <div 
              key={pos}
              className="connection"
              style={{ left: `${pos}%` }}
            />
          ))}
        </div>
      </div>

      {/* Main Content */}
      <div className="electrician-content">
        <div className="tool-icon">
          <div className="screwdriver" />
          <div className="pliers" />
        </div>

        <h1 className="voltage-display">
          {voltage}V
          <span className="voltage-label">Live Circuit</span>
        </h1>

        <div className="circuit-loader">
          <div className="wire-progress" style={{ width: `${wireProgress}%` }} />
          <div className="wire-ends" />
        </div>

        <p className="electrician-tagline">
          {businessName || "Professional Electrical Services"}
          <br />
          <span className="safety-message">Certified & Insured</span>
        </p>
      </div>

      {/* Safety Badges */}
      <div className="safety-badges">
        <div className="certification-badge">
          <span className="ohm-symbol">Ω</span>
          <span>Certified</span>
        </div>
        <div className="certification-badge">
          <span className="voltage-symbol">⚡</span>
          <span>240V Rated</span>
        </div>
      </div>
    </div>
  );
};

export default LoadingScreen;
