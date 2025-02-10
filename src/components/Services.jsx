import React, { useEffect, useRef, useContext, useState } from 'react';
import { ThemeContext } from '../App';
import './Services.css';

function Services({ business }) {
  const { color1, color2, phone } = business.businessInfo;
  const servicesRef = useRef(null);
  const { isDark } = useContext(ThemeContext);
  // Add state to track visible cards
  const [visibleCards, setVisibleCards] = useState(new Set());

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            setVisibleCards(prev => new Set([...prev, entry.target.dataset.index]));
          }
        });
      },
      {
        threshold: 0.1,
        rootMargin: '50px'
      }
    );

    const cards = document.querySelectorAll('.service-card');
    cards.forEach(card => observer.observe(card));

    return () => {
      cards.forEach(card => observer.unobserve(card));
    };
  }, []);

  const services = [
    {
      title: "Residential Services",
      description: "Complete home electrical solutions including installations, repairs, and upgrades for your peace of mind.",
      icon: "⚡",
    },
    {
      title: "Commercial Services",
      description: "Professional electrical installations and maintenance for businesses of all sizes.",
      icon: "🏢",
    },
    {
      title: "Emergency Service",
      description: "24/7 emergency electrical repairs and support when you need it most.",
      icon: "🚨",
    },
    {
      title: "Panel Upgrades",
      description: "Electrical panel replacements and capacity upgrades to meet your power needs.",
      icon: "🔌",
    },
    {
      title: "Safety Inspections",
      description: "Comprehensive electrical safety audits and certification services.",
      icon: "✓",
    },
    {
      title: "Lighting Design",
      description: "Custom lighting solutions to enhance your space with modern, efficient fixtures.",
      icon: "💡",
    },
  ];

  return (
    <section 
      id="services" 
      className={`services-section ${isDark ? 'theme-dark' : 'theme-light'}`} 
      ref={servicesRef}
    >
      <div className="services-header">
        <h2 style={{ color: color1 || '#3498db' }}>
          Our Services
        </h2>
        <p>
          Contact us for a complete list of our professional electrical services and solutions
        </p>
      </div>
      <div className="services-grid">
        {services.map((service, index) => (
          <div
            key={index}
            data-index={index}
            className={`service-card ${isDark ? 'theme-dark' : 'theme-light'} ${
              visibleCards.has(index.toString()) ? 'visible' : ''
            }`}
            style={{
              '--card-color': color1 || '#3498db',
            }}
          >
            <div 
              className="service-icon"
              style={{ color: color1 || '#3498db' }}
            >
              {service.icon}
            </div>
            <div className="service-details">
              <h3>{service.title}</h3>
              <p>{service.description}</p>
            </div>
            <div className="service-contact">
              <a
                href={`tel:${phone}`}
                className="contact-button"
                style={{
                  background: `linear-gradient(45deg, ${color1 || '#3498db'}, ${color2 || '#2980b9'})`,
                  boxShadow: `0 4px 15px ${color1 ? color1 + '4D' : 'rgba(52, 152, 219, 0.3)'}`,
                }}
              >
                Call Us: {phone}
              </a>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

export default Services;