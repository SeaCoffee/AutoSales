import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

const AllListingsList = () => {
  const [listings, setListings] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    axios.get('/api/listings/list/')
      .then(response => {
        setListings(response.data.data);
      })
      .catch(() => setError('Failed to load listings'));
  }, []);

  const containerStyle = {
    padding: '20px',
    maxWidth: '800px',
    margin: 'auto'
  };

  const listStyle = {
    listStyleType: 'none',
    padding: 0
  };

  const listItemStyle = {
    padding: '10px',
    margin: '10px 0',
    border: '1px solid #ccc',
    borderRadius: '5px',
    backgroundColor: '#f9f9f9',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center'
  };

  const linkStyle = {
    textDecoration: 'none',
    color: '#007bff',
    marginTop: '10px'
  };

  const errorStyle = {
    color: 'red',
    fontWeight: 'bold'
  };

  const imgStyle = {
  maxWidth: '200px',
  height: 'auto',
  borderRadius: '8px',
  margin: '20px 0',
};


  return (
    <div style={containerStyle}>
      <h2>Car Listings</h2>
      {error && <p style={errorStyle}>{error}</p>}
      <ul style={listStyle}>
        {listings.length > 0 ? (
          listings.map(listing => (
            <li key={listing.id} style={listItemStyle}>
              <h3>{listing.title}</h3>
              <p>{listing.description}</p>
              {listing.listing_photo && (
                <img src={listing.listing_photo} alt={listing.title} style={imgStyle} />
              )}
              <div>
                <Link to={`/alllistingsdetails/${listing.id}`} style={linkStyle}>View Details</Link>
              </div>
            </li>
          ))
        ) : (
          <p>No listings available.</p>
        )}
      </ul>
    </div>
  );
};

export default AllListingsList;


