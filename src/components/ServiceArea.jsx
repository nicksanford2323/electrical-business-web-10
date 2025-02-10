import React from 'react';
import './ServiceArea.css';

function ServiceArea({ business }) {
  const { latitude, longitude, city, state, full_address } = business.businessInfo;

  // Calculate bounding box for OpenStreetMap
  const bbox = {
    minLon: longitude - 0.5,
    minLat: latitude - 0.5,
    maxLon: longitude + 0.5,
    maxLat: latitude + 0.5
  };

  // Example service cities - you would customize per business
  const serviceCities = [
    `${city}, ${state}`,
    "Nearby City 1",
    "Nearby City 2",
    "Nearby City 3",
    "Nearby City 4",
    "Nearby City 5"
  ];

  return (
    <section className="service-area">
      <h2>Areas We Serve</h2>

      <div className="service-container">
        {/* Left side: City list */}
        <div className="city-list">
          <ul>
            {serviceCities.map((city, index) => (
              <li key={index}>
                <span className="star">★</span> {city}
              </li>
            ))}
          </ul>
        </div>

        {/* Right side: Map */}
        <div className="map-wrapper">
          <iframe
            title="Service Area Map"
            width="100%"
            height="100%"
            frameBorder="0"
            scrolling="no"
            src={`https://www.openstreetmap.org/export/embed.html?bbox=${bbox.minLon},${bbox.minLat},${bbox.maxLon},${bbox.maxLat}&layer=mapnik&marker=${latitude},${longitude}`}
          />

          {/* Blue overlay to show service area */}
          <div className="map-overlay">
            <div className="service-radius"></div>
          </div>
        </div>
      </div>

      {/* Service area disclaimer */}
      <div className="service-disclaimer">
        <p>Our main office is located at: {full_address}</p>
        <p>We service all surrounding areas. Contact us to confirm service availability in your location.</p>
      </div>
    </section>
  );
}

export default ServiceArea;