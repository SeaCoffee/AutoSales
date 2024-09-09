import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { FaComment } from 'react-icons/fa';
import axios from 'axios';

const ListingsUserList = () => {
  const [listings, setListings] = useState([]);
  const [error, setError] = useState('');
  const [socket, setSocket] = useState(null);
  const [chatMessages, setChatMessages] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    axios.get('api/listings/user/')
      .then(response => {
        console.log('Listings:', response.data.data);
        setListings(response.data.data);
      })
      .catch(() => setError('Failed to load listings'));
  }, []);

  // Подключение к WebSocket
  useEffect(() => {
    if (listings.length > 0) {
      const connectToSocket = async () => {
        try {
          const socketToken = await axios.get('/api/auth/soket/');
          if (socketToken) {
            const listingId = listings[0].id;
            const newSocket = new WebSocket(`ws://localhost/api/chat/${listingId}/?token=${socketToken.data.token}`);

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
        } catch (error) {
          console.error('Failed to connect to WebSocket:', error);
        }
      };

      connectToSocket();
    }

    return () => {
      if (socket) {
        console.log('Disconnecting WebSocket for chat');
        socket.close();
      }
    };
  }, [listings]);

  const openChat = (listingId) => {
    navigate(`/chat/${listingId}`);
    if (socket) {
      socket.close(); // Закрываем текущее соединение перед открытием нового чата
    }

    const connectToSocket = async () => {
      try {
        const socketToken = await axios.get('/api/auth/soket/');
        if (socketToken) {
          const newSocket = new WebSocket(`ws://localhost/api/chat/${listingId}/?token=${socketToken.data.token}`);

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
      } catch (error) {
        console.error('Failed to connect to WebSocket:', error);
      }
    };

    connectToSocket(); // Подключаемся к новому чату
  };

  if (error) {
    return <p>{error}</p>;
  }

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
    margin: '5px 0',
    border: '1px solid #ccc',
    borderRadius: '5px',
    backgroundColor: '#f9f9f9'
  };

  const linkStyle = {
    textDecoration: 'none',
    color: '#007bff',
    marginLeft: '15px',
  };

  const errorStyle = {
    color: 'red',
    fontWeight: 'bold'
  };

  const buttonStyle = {
    marginTop: '10px',
    padding: '10px 20px',
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    cursor: 'pointer',
    borderRadius: '8px',
  };

  const imgStyle = {
  maxWidth: '300px',
  height: 'auto',
  borderRadius: '8px',
  margin: '20px 0',
};


  return (
    <div style={containerStyle}>
      <h2>Your Listings</h2>
      {error && <p style={errorStyle}>{error}</p>}
      <ul style={listStyle}>
        {listings.map(listing => (
          <li key={listing.id} style={listItemStyle}>
            {listing.title} - {listing.description}
            <Link to={`/listings/update/${listing.id}`} style={linkStyle}>Edit</Link>
            <Link to={`/listingsuserdetails/${listing.id}`} style={linkStyle}>View</Link>
            <Link to={`/delete/${listing.id}`} style={linkStyle}>Delete</Link>
            <button onClick={() => openChat(listing.id)} style={buttonStyle}>
              <FaComment /> Open Chat
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ListingsUserList;


