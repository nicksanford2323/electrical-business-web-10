import React, { useState, useContext, useEffect } from 'react';
import { ThemeContext } from '../App';
import './Header.css';

function Header({ business }) {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isSticky, setIsSticky] = useState(false);
  const { isDark, toggleTheme } = useContext(ThemeContext);

  // Extract business info
  const { businessName } = business;
  const { phone, rating, reviews, reviews_link, color1, color2 } = business.businessInfo;
  const showReviews = parseFloat(rating) >= 4.5 && parseInt(reviews) >= 8;
  const primaryColor = color1 || '#4a90e2';
  const secondaryColor = color2 || '#357abd';

  // Use a smaller threshold for sticky header
  useEffect(() => {
    const handleScroll = () => {
      setIsSticky(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <div className={`header-wrapper ${isSticky ? 'sticky' : ''}`}>
      {/* Clickable CTA Banner */}
      <a className="cta-banner" style={{ backgroundColor: primaryColor }} href={`tel:${phone}`}>
        FREE QUOTE: {phone}
      </a>

      <header className={`header ${isDark ? 'theme-dark' : 'theme-light'}`}>
        {/* Business Name (logo placeholder) */}
        <div className="business-name">
          <h1>{businessName}</h1>
          <small className="logo-placeholder">(Logo would be here)</small>
        </div>

        {/* Navigation */}
        <nav className={`nav-links ${isMenuOpen ? 'active' : ''}`}>
          <ul style={{ '--hover-color': secondaryColor }}>
            <li><a href="#hero">Home</a></li>
            <li><a href="#about">About</a></li>
            <li><a href="#services">Services</a></li>
            <li><a href="#gallery">Gallery</a></li>
            <li><a href="#location">Location</a></li>
            <li><a href="#contact">Contact</a></li>
          </ul>
        </nav>

        {/* Header Actions */}
        <div className="header-actions">
          {showReviews && (
            <a 
              href={reviews_link} 
              className="google-review" 
              target="_blank" 
              rel="noopener noreferrer"
            >
              <div className="stars">
                {[...Array(5)].map((_, i) => (
                  <span key={i} className={i < Math.floor(rating) ? 'star filled' : 'star'}>
                    ★
                  </span>
                ))}
              </div>
              <span className="review-count">{rating} ({reviews} reviews)</span>
            </a>
          )}
          <button 
            onClick={toggleTheme} 
            className="theme-toggle" 
            aria-label={`Switch to ${isDark ? 'light' : 'dark'} mode`}
            title="Toggle site theme"
          >
            <span className="toggle-icon">{isDark ? '☀️' : '🌙'}</span>
          </button>
        </div>

        {/* Mobile Menu Button */}
        <div 
          className={`menu-button ${isMenuOpen ? 'open' : ''}`}
          onClick={() => setIsMenuOpen(!isMenuOpen)}
        >
          <span></span>
          <span></span>
          <span></span>
        </div>
      </header>
    </div>
  );
}

export default Header;
