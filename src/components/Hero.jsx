import React, { useState, useEffect } from 'react';
import './Hero.css';

function Hero({ business }) {
  const [currentSlide, setCurrentSlide] = useState(0);
  const [isTransitioning, setIsTransitioning] = useState(false);
  const heroSlides = business.sections.hero;
  const { phone, color1, color2 } = business.businessInfo;

  // Auto-advance slides
  useEffect(() => {
    const timer = setInterval(() => {
      setIsTransitioning(true);
      setTimeout(() => {
        setCurrentSlide((prev) => (prev + 1) % heroSlides.length);
        setIsTransitioning(false);
      }, 500);
    }, 5000);
    return () => clearInterval(timer);
  }, [heroSlides.length]);

  // Get button config for current slide
  const getButtonConfig = (index) => {
    switch(index % 3) {
      case 0:
        return {
          text: `Call Now: ${phone}`,
          action: () => window.location.href = `tel:${phone}`
        };
      case 1:
        return {
          text: 'Get a Quote',
          action: () => document.getElementById('contact')?.scrollIntoView({ behavior: 'smooth' })
        };
      case 2:
        return {
          text: 'View Gallery',
          action: () => document.getElementById('gallery')?.scrollIntoView({ behavior: 'smooth' })
        };
      default:
        return null;
    }
  };

  const buttonConfig = getButtonConfig(currentSlide);

  return (
    <section className="hero-section">
      {/* Background Image */}
      <div 
        className={`hero-background ${isTransitioning ? 'fade-out' : ''}`}
        style={{
          backgroundImage: `url(${heroSlides[currentSlide].imageIndex})`
        }}
      />
      {/* Content Overlay */}
      <div className="hero-content">
        <h1>{business.businessName}</h1>
        <p className="hero-text">{heroSlides[currentSlide].callToAction}</p>

        {/* Action Button */}
        {buttonConfig && (
          <button 
            className="hero-button"
            onClick={buttonConfig.action}
            style={{
              backgroundColor: color1 || '#4a90e2',
              borderColor: color2 || '#357abd'
            }}
          >
            {buttonConfig.text}
          </button>
        )}

        {/* Slide Indicators */}
        <div className="slide-indicators">
          {heroSlides.map((_, index) => (
            <button
              key={index}
              onClick={() => setCurrentSlide(index)}
              className={`slide-dot ${currentSlide === index ? 'active' : ''}`}
              aria-label={`Go to slide ${index + 1}`}
            />
          ))}
        </div>
      </div>
    </section>
  );
}

export default Hero;