import React, { useState, useEffect, useCallback, useContext } from 'react';
import { ThemeContext } from '../App';
import './Reviews.css';

function Reviews({ business }) {
  const { isDark } = useContext(ThemeContext);
  if (!business) return null;

  const { 
    rating: ratingStr, 
    reviews: reviewCountStr, 
    reviews_link: reviewsLink 
  } = business.businessInfo || {};

  const rating = parseFloat(ratingStr) || 0;
  const reviewCount = parseInt(reviewCountStr, 10) || 0;
  const allReviews = business.reviews || [];

  const filteredReviews = allReviews.filter(
    review => review.review_text && review.review_text.trim() !== ""
  );

  const businessName = business.businessName || '';

  if (filteredReviews.length === 0) return null;

  const [currentReview, setCurrentReview] = useState(0);
  const [isPaused, setIsPaused] = useState(false);

  const nextReview = useCallback(() => {
    setCurrentReview(current => (current + 1) % filteredReviews.length);
  }, [filteredReviews.length]);

  const prevReview = useCallback(() => {
    setCurrentReview(current => (current - 1 + filteredReviews.length) % filteredReviews.length);
  }, [filteredReviews.length]);

  useEffect(() => {
    if (!isPaused) {
      const timer = setInterval(nextReview, 5000);
      return () => clearInterval(timer);
    }
  }, [isPaused, nextReview]);

  return (
    <section className={`reviews-section ${isDark ? 'theme-dark' : 'theme-light'}`}>
      <div className="reviews-header">
        <h2>{businessName} Reviews</h2>
        <div className="overall-rating">
          <div className="stars">★★★★★</div>
          <p className="rating-text">{rating} out of 5 stars based on {reviewCount} reviews</p>
        </div>
      </div>

      <div 
        className="reviews-slideshow"
        onMouseEnter={() => setIsPaused(true)}
        onMouseLeave={() => setIsPaused(false)}
      >
        <div 
          className="reviews-track"
          style={{ transform: `translateX(-${currentReview * 100}%)` }}
        >
          {filteredReviews.map((review, index) => (
            <div className="review-slide" key={index}>
              <div className="review-card">
                <div className="reviewer-info">
                  <h3>{review.reviewer_name || 'Customer Review'}</h3>
                  <div className="review-stars">★★★★★</div>
                </div>
                <p className="review-text">{review.review_text}</p>
              </div>
            </div>
          ))}
        </div>

        <button className="nav-button prev" onClick={prevReview}>
          &#8249;
        </button>
        <button className="nav-button next" onClick={nextReview}>
          &#8250;
        </button>
      </div>

      <div className="reviews-cta">
        <p>Share your experience with our services</p>
        <a 
          href={reviewsLink || '#'} 
          target="_blank" 
          rel="noopener noreferrer"
          className="review-button"
        >
          Leave Us a Review
        </a>
      </div>
    </section>
  );
}

export default Reviews;