import React, { useState, useEffect, useCallback, useContext } from 'react';
import { ThemeContext } from '../App'; // Adjust path if needed
import './Gallery.css';

function Gallery({ business }) {
  const { isDark } = useContext(ThemeContext);

  // Get gallery images and brand colors from business data
  const images = business.sections.gallery || [];
  const { color1, color2 } = business.businessInfo || {};

  // Default colors if none provided
  const primaryColor = color1 || '#4a90e2';
  const secondaryColor = color2 || '#357abd';

  const [currentSlide, setCurrentSlide] = useState(0);
  const [isPaused, setIsPaused] = useState(false);
  const [showControls, setShowControls] = useState(false);

  const nextSlide = useCallback(() => {
    setCurrentSlide(current => (current + 1) % images.length);
  }, [images.length]);

  const prevSlide = useCallback(() => {
    setCurrentSlide(current => (current - 1 + images.length) % images.length);
  }, [images.length]);

  // Auto-advance slides every 2.5 seconds if not paused
  useEffect(() => {
    if (!isPaused) {
      const timer = setInterval(nextSlide, 2500);
      return () => clearInterval(timer);
    }
  }, [isPaused, nextSlide]);

  // Hide navigation controls after 3 seconds of inactivity
  useEffect(() => {
    if (showControls) {
      const timer = setTimeout(() => setShowControls(false), 3000);
      return () => clearTimeout(timer);
    }
  }, [showControls]);

  return (
    <section className={`gallery-section ${isDark ? 'theme-dark' : 'theme-light'}`}>
      <div className="gallery-header">
        <h2>Our Project Portfolio</h2>
        <div 
          className="title-underline"
          style={{ backgroundColor: primaryColor }}
        ></div>
        <p>
          {isDark
            ? 'Discover the quality and innovation behind our electrical solutions.'
            : 'Experience our craftsmanship and attention to detail in every project.'}
        </p>
      </div>

      <div 
        className="slideshow-container"
        onMouseEnter={() => {
          setIsPaused(true);
          setShowControls(true);
        }}
        onMouseLeave={() => {
          setIsPaused(false);
          setShowControls(false);
        }}
        onMouseMove={() => setShowControls(true)}
      >
        <div 
          className="slides-wrapper" 
          style={{ transform: `translateX(-${currentSlide * 100}%)` }}
        >
          {images.map((img, index) => (
            <div key={index} className="slide">
              <img src={img} alt={`Project ${index + 1}`} />
              <div className="slide-overlay"></div>
            </div>
          ))}
        </div>

        <button 
          className={`nav-button prev ${showControls ? 'visible' : ''}`}
          onClick={prevSlide}
          style={{ '--hover-bg': primaryColor }}
        >
          &#8249;
        </button>

        <button 
          className={`nav-button next ${showControls ? 'visible' : ''}`}
          onClick={nextSlide}
          style={{ '--hover-bg': primaryColor }}
        >
          &#8250;
        </button>

        <div 
          className="slide-counter"
          style={{ 
            backgroundColor: `${primaryColor}cc`,
            border: `2px solid ${secondaryColor}`
          }}
        >
          {currentSlide + 1} / {images.length}
        </div>
      </div>
    </section>
  );
}

export default Gallery;
