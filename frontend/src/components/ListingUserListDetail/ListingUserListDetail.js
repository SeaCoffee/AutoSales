import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';


const ListingUserListDetail = () => {
  const { id } = useParams();
  const [listing, setListing] = useState(null);
  const [error, setError] = useState('');



  useEffect(() => {
    axios.get(`/api/listings/cardetails/${id}/`)
      .then(response => {
        setListing(response.data);
      })
      .catch(error => setError('Failed to load listing details'));
  }, [id]);



  if (error) {
    return <p>{error}</p>;
  }

  if (!listing) {
    return <p>Loading...</p>;
  }

  const containerStyle = {
    padding: '20px',
    maxWidth: '600px',
    margin: 'auto',
    border: '1px solid #ccc',
    borderRadius: '8px',
    backgroundColor: '#f9f9f9',
    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
  };

  const imgStyle = {
  maxWidth: '300px',
  height: 'auto',
  borderRadius: '8px',
  margin: '20px 0',
};

  const titleStyle = {
    fontSize: '24px',
    marginBottom: '10px',
    color: '#333',
  };

  const priceStyle = {
    fontSize: '18px',
    fontWeight: 'bold',
    margin: '10px 0',
  };

  const detailStyle = {
    fontSize: '16px',
    marginBottom: '10px',
    color: '#555',
  };

  const chatContainerStyle = {
    marginTop: '20px',
    padding: '10px',
    backgroundColor: '#e9ecef',
    borderRadius: '8px',
  };

  const chatBoxStyle = {
    height: '200px',
    overflowY: 'scroll',
    border: '1px solid #ddd',
    marginBottom: '10px',
    padding: '10px',
    backgroundColor: '#fff',
    borderRadius: '8px',
  };

  const inputStyle = {
    width: 'calc(100% - 22px)',
    padding: '10px',
    marginBottom: '10px',
  };

  const buttonStyle = {
    padding: '10px 20px',
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    cursor: 'pointer',
    borderRadius: '8px',
  };

  return (
    <div style={containerStyle}>
      <h2 style={titleStyle}>{listing.title}</h2>
      <p style={detailStyle}>{listing.description}</p>
      <p style={priceStyle}>Price: {listing.price} {listing.currency}</p>
      <img src={listing.listing_photo} alt={listing.title} style={imgStyle} />
    </div>
  );
};

export default ListingUserListDetail;
