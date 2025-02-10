import React, { useState, useEffect, useContext } from 'react';
import { ThemeContext } from '../App'; // Make sure ThemeContext is set up in your App
import './About.css';

const About = ({ business }) => {
  const { isDark } = useContext(ThemeContext);

  // Get business information with fallbacks
  const businessName = business?.businessName || 'Your Business';
  const phone = business?.businessInfo?.phone || '+1 (555) 123-4567';
  const city = business?.businessInfo?.city;
  // Fallback if city is not available
  const serviceArea = city ? `${city} and surrounding areas` : 'your local area';

  // Hardcoded About text including licensing/insurance and local ownership
  const aboutText = `Welcome to ${businessName}! We are a licensed, insured, and locally owned & operated electrical service provider. We proudly serve ${serviceArea} with top-notch electrical services. Our highly trained team is dedicated to providing safe, efficient, and reliable solutions for both residential and commercial projects. Call us today at ${phone} to schedule your appointment or get a free quote!`;

  // Retrieve slideshow images from business data if available; otherwise use fallbacks.
  let images = [];
  if (business?.sections?.aboutUs && business.sections.aboutUs.length >= 2) {
    images = [
      business.sections.aboutUs[0].imageIndex,
      business.sections.aboutUs[1].imageIndex
    ];
  } else {
    images = [
      'https://placehold.co/600x400/111/fff?text=Electrician+1',
      'https://placehold.co/600x400/222/fff?text=Electrician+2'
    ];
  }

  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    // Toggle images every 5 seconds
    const interval = setInterval(() => {
      setCurrentIndex(prevIndex => (prevIndex === 0 ? 1 : 0));
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className={`about-section ${isDark ? 'theme-dark' : 'theme-light'}`}>
      <div className="about-content">
        {/* Slideshow Container */}
        <div className="about-slideshow">
          <img
            src={images[currentIndex]}
            alt={`About ${businessName}`}
            className="about-image"
          />
        </div>
        {/* Text Container */}
        <div className="about-info">
          <h2>About {businessName}</h2>
          <p>{aboutText}</p>
          <a href={`tel:${phone}`} className="electric-button">
            Call Us: {phone}
          </a>
        </div>
      </div>
    </div>
  );
};

export default About;
