import React, { useContext } from 'react';
import { ThemeContext } from '../App';
import './Footer.css';

function Footer({ business }) {
  const { isDark } = useContext(ThemeContext);
  if (!business) return null;

  const { 
    phone, 
    email, 
    full_address,
    working_hours,
    license,
  } = business.businessInfo || {};

  // Parse working hours if available
  let parsedHours = {};
  try {
    parsedHours = working_hours ? JSON.parse(working_hours) : null;
  } catch (e) {
    console.error('Error parsing working hours:', e);
  }

  const currentYear = new Date().getFullYear();
  const businessName = business.businessName || '';

  // Check if business operates 24/7
  const is24_7 = parsedHours && Object.values(parsedHours).some(hours => 
    hours.includes('24 hours') || hours.includes('24/7')
  );

  return (
    <footer className={`footer ${isDark ? 'theme-dark' : 'theme-light'}`}>
      <div className="footer-grid">
        {/* Company Info */}
        <div className="footer-section">
          <h3>{businessName}</h3>
          <p className="slogan">Your Trusted Electrical Service Partner</p>
          <div className="company-details">
            {license && (
              <p className="license">License #: {license}</p>
            )}
            <p className="service-area">Serving Birmingham & Surrounding Areas</p>
          </div>
        </div>

        {/* Contact Info */}
        <div className="footer-section">
          <h3>Contact Us</h3>
          <div className="contact-details">
            {is24_7 && <p>24/7 Emergency Service</p>}
            <a href={`tel:${phone}`} className="contact-link">
              📞 {phone}
            </a>
            {email && (
              <a href={`mailto:${email}`} className="contact-link">
                ✉️ {email}
              </a>
            )}
            {full_address && (
              <p className="address">
                📍 {full_address}
              </p>
            )}
          </div>
        </div>

        {/* Services */}
        <div className="footer-section">
          <h3>Our Services</h3>
          <ul className="services-list">
            <li>Residential Electrical</li>
            <li>Commercial Services</li>
            <li>Emergency Repairs</li>
            <li>Electrical Inspections</li>
            <li>Panel Upgrades</li>
            <li>Lighting Installation</li>
          </ul>
        </div>

        {/* Hours */}
        <div className="footer-section">
          <h3>Business Hours</h3>
          <div className="hours-container">
            {parsedHours ? (
              Object.entries(parsedHours).map(([day, hours]) => (
                <p key={day} className="hours-row">
                  <span className="day">{day}:</span>
                  <span className="hours">{hours}</span>
                </p>
              ))
            ) : (
              <>
                <p>Monday - Friday: 8AM - 5PM</p>
                <p>Saturday - Sunday: Closed</p>
              </>
            )}
            {is24_7 && (
              <div className="emergency-callout">
                <p className="emergency-text">24/7 Emergency Service Available</p>
                <a href={`tel:${phone}`} className="emergency-button">
                  Call Now
                </a>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="footer-bottom">
        <div className="footer-bottom-content">
          <p>
            © {currentYear} {businessName}. All Rights Reserved
            {license && <span className="license-number"> | License #{license}</span>}
          </p>
          <div className="footer-links">
            <a href="/privacy">Privacy Policy</a>
            <a href="/terms">Terms of Service</a>
          </div>
        </div>
      </div>
    </footer>
  );
}

export default Footer;