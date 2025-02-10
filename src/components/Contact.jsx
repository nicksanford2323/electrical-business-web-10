import React, { useContext } from 'react';
import { ThemeContext } from '../App';
import './Contact.css';

function Contact({ business }) {
  const { isDark } = useContext(ThemeContext);
  const businessName = business.businessName || 'Our Business';

  return (
    <section id="contact" className={`contact-section ${isDark ? 'theme-dark' : 'theme-light'}`}>
      <div className="contact-container">
        <div className="contact-header">
          <h2>Get in Touch</h2>
          <p>
            Tell us about your next electrical project, or get a quick quote for any electrical services you need.
          </p>
        </div>

        <form className="contact-form">
          <div className="form-group">
            <label htmlFor="name">Name</label>
            <input 
              type="text" 
              id="name" 
              placeholder="Your Name" 
              required 
            />
          </div>

          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input 
              type="email" 
              id="email" 
              placeholder="Your Email" 
              required 
            />
          </div>

          <div className="form-group">
            <label htmlFor="message">Message</label>
            <textarea 
              id="message" 
              placeholder="Tell us about your project or service needs..." 
              required
              rows="6"
            ></textarea>
          </div>

          <button type="submit" className="submit-button">
            Send Message
          </button>
        </form>
      </div>
    </section>
  );
}

export default Contact;