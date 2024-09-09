import React from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';


const DeleteListingPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [error, setError] = React.useState('');

  const handleDelete = () => {
  axios.delete(`/api/listings/delete/${id}/`)
      .then(() => {
        navigate('/listingsuserlist');
      })
      .catch(err => {
        setError('Failed to delete listing');
      });
  };

  const containerStyle = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
    backgroundColor: '#f8f9fa',
    padding: '20px',
  };

  const headingStyle = {
    fontSize: '24px',
    marginBottom: '20px',
    textAlign: 'center',
  };

  const buttonContainerStyle = {
    display: 'flex',
    gap: '10px',
  };

  const buttonStyle = {
    padding: '10px 20px',
    fontSize: '16px',
    borderRadius: '8px',
    border: 'none',
    cursor: 'pointer',
  };

  const deleteButtonStyle = {
    ...buttonStyle,
    backgroundColor: '#dc3545',
    color: 'white',
  };

  const cancelButtonStyle = {
    ...buttonStyle,
    backgroundColor: '#6c757d',
    color: 'white',
  };

  const errorStyle = {
    color: 'red',
    marginTop: '20px',
  };

  return (
    <div style={containerStyle}>
      <h2 style={headingStyle}>Are you sure you want to delete this listing?</h2>
      {error && <p style={errorStyle}>{error}</p>}
      <div style={buttonContainerStyle}>
        <button onClick={handleDelete} style={deleteButtonStyle}>Yes, Delete</button>
        <button onClick={() => navigate('/listingsuser')} style={cancelButtonStyle}>Cancel</button>
      </div>
    </div>
  );
};

export default DeleteListingPage;

