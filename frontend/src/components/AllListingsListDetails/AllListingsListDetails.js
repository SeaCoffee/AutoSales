import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';


const AllListingsListDetails = () => {
  const { id } = useParams();
  const [listing, setListing] = useState(null);
  const [stats, setStats] = useState(null);
  const [error, setError] = useState('');
  const [userData, setUserData] = useState(null);
  const [message, setMessage] = useState('');
  const [chatMessages, setChatMessages] = useState([]);
  const [socket, setSocket] = useState(null);

  // Маппинг ID валют к обозначениям
  const currencySymbols = {
    1: '$',  // USD
    2: '€',  // EUR
    3: '₴',  // UAH
    // Добавьте другие валюты, если нужно
  };

  useEffect(() => {
    console.log('Attempting to decode token...');
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const decodedToken = jwtDecode(token);
        console.log('Token decoded:', decodedToken);
        setUserData(decodedToken);

        // Получение данных объявления
        axios.get(`/api/listings/cardetails/${id}/`)
          .then(response => {
            console.log('Listing data:', response.data);
            setListing(response.data);
          })
          .catch(error => {
            console.error('Failed to load listing details:', error);
            setError('Failed to load listing details');
          });

        if (decodedToken.account_type === 'premium') {
          console.log('Fetching statistics...');
          axios.get(`/api/listings/premium/${id}/stats/`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`
            }
          })
            .then(response => {
              console.log('Stats data:', response.data);
              setStats(response.data);
            })
            .catch(error => {
              console.error('Failed to load statistics:', error);
              setError('Failed to load statistics');
            });
        }

      } catch (error) {
        console.error('Failed to decode token:', error);
      }
    } else {
      console.error('Token not found');
    }
  }, [id]);

  // Подключение к WebSocket
  useEffect(() => {
    const connectToSocket = async () => {
      const socketToken = await axios.get('/api/auth/soket/');
      if (socketToken) {
        const newSocket = new WebSocket(`ws://localhost/api/chat/${id}/?token=${socketToken.data.token}`);

        newSocket.onopen = () => {
          console.log('WebSocket connected');
        };

        newSocket.onmessage = (event) => {
          const messageData = JSON.parse(event.data);
          setChatMessages((prevMessages) => [...prevMessages, messageData]);
        };

        newSocket.onclose = () => {
          console.log('WebSocket disconnected');
        };

        setSocket(newSocket);
      }
    };

    connectToSocket();

    return () => {
      if (socket) {
        socket.close();
      }
    };
  }, [id]);


  useEffect(() => {
    console.log('Current stats state:', stats);
  }, [stats]);

  const sendMessage = () => {
    if (socket && message.trim()) {
      socket.send(JSON.stringify({
        action: 'send_message',
        data: message,
        request_id: id
      }));
      setChatMessages((prevMessages) => [...prevMessages, { message: message, user: 'You' }]);
      setMessage('');
    }
  };

  if (error) {
    return <p>{error}</p>;
  }

  if (!listing) {
    return <p>Loading listing...</p>;
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

  const statsContainerStyle = {
    marginTop: '20px',
    padding: '10px',
    backgroundColor: '#e9ecef',
    borderRadius: '8px',
  };

  const statItemStyle = {
    marginBottom: '8px',
    fontSize: '16px',
  };

  return (
    <div style={containerStyle}>
      <h2 style={titleStyle}>{listing.title}</h2>
      <p style={detailStyle}>{listing.description}</p>
      <p style={priceStyle}>Price: {listing.price} {currencySymbols[listing.currency] || listing.currency}</p>
      <p style={detailStyle}>Year: {listing.year}</p>
      <p style={detailStyle}>Engine: {listing.engine}</p>
      {listing.listing_photo && (
        <img
          src={listing.listing_photo}
          alt={listing.title}
          style={imgStyle}
        />
      )}
      <p style={detailStyle}>Initial Rate: {listing.initial_currency_rate}</p>
      <p style={detailStyle}>Current Rate: {listing.current_currency_rate}</p>

      {stats && (
        <div style={statsContainerStyle}>
          <h3>Statistics</h3>
          <p style={statItemStyle}>Total Views: {stats.total_views || 'N/A'}</p>
          <p style={statItemStyle}>Average Price in Region: {stats.average_price_by_region || 'N/A'}</p>
          <p style={statItemStyle}>Average Price in Country: {stats.average_price_by_country || 'N/A'}</p>
        </div>
      )}

      <div>
        <h3>Listing chat</h3>
        <div>
          {chatMessages.map((msg, index) => (
            <div key={index}>{msg.user}: {msg.message}</div>
          ))}
        </div>
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default AllListingsListDetails;

