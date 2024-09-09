import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate, useParams } from 'react-router-dom';

const UpdateListingPage = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const [listing, setListing] = useState({
    title: '',
    description: '',
    price: '',
    currency: '',
    listing_photo: null, // Это для новой фотографии
    listing_photo_url: '', // Это для текущего URL фото
  });
  const [error, setError] = useState('');

  useEffect(() => {
    // Получаем данные объявления
    axios.get(`/api/listings/details/${id}/`)
      .then(response => {
        setListing({
          ...response.data,
          listing_photo_url: response.data.listing_photo, // Предположительно URL текущей фотографии
        });
      })
      .catch(error => setError('Failed to load listing data'));
  }, [id]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setListing({ ...listing, [name]: value });
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0]; // Получаем файл
    if (file) {
        setListing({ ...listing, listing_photo: file });
    }
};


const handleSubmit = (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('title', listing.title);
    formData.append('description', listing.description);
    formData.append('price', listing.price);
    formData.append('currency', listing.currency);

    // Проверяем, является ли listing_photo объектом файла (а не URL)
    if (listing.listing_photo instanceof File) {
        formData.append('listing_photo', listing.listing_photo);
    }

    // Логируем содержимое formData для проверки, что именно отправляется
    for (let [key, value] of formData.entries()) {
        console.log(`${key}: ${value}`);
    }

    axios.put(`/api/listings/update/${id}/`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    })
    .then(() => navigate('/listingsuserlist'))
    .catch(error => {
        const serverError = error.response?.data || 'Failed to update listing';
        setError(serverError);
        console.error('Error updating listing:', serverError);
    });
};




  const formStyle = {
    display: 'flex',
    flexDirection: 'column',
    maxWidth: '500px',
    margin: 'auto',
    gap: '10px',
  };

  const inputStyle = {
    padding: '8px 10px',
    border: '1px solid #ccc',
    borderRadius: '4px',
    fontSize: '16px'
  };

  const labelStyle = {
    marginBottom: '5px',
    fontWeight: 'bold'
  };

  const buttonStyle = {
    padding: '10px 15px',
    backgroundColor: '#4CAF50',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '16px'
  };

  const errorStyle = {
    color: 'red',
    fontWeight: 'bold'
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Update Listing</h2>
      <form onSubmit={handleSubmit} style={formStyle}>
        <label style={labelStyle}>Title</label>
        <input type="text" name="title" value={listing.title} onChange={handleChange} style={inputStyle} />

        <label style={labelStyle}>Description</label>
        <textarea name="description" value={listing.description} onChange={handleChange} style={{ ...inputStyle, height: '100px' }} />

        <label style={labelStyle}>Price</label>
        <input type="number" name="price" value={listing.price} onChange={handleChange} style={inputStyle} />

        <label style={labelStyle}>Currency</label>
        <input type="text" name="currency" value={listing.currency} onChange={handleChange} style={inputStyle} />


        <label style={labelStyle}>Update Photo</label>
        <input type="file" name="listing_photo" onChange={handleFileChange} style={inputStyle} />

        <button type="submit" style={buttonStyle}>Update</button>
      </form>
      {error && <p style={errorStyle}>{error}</p>}
    </div>
  );
};

export default UpdateListingPage;

