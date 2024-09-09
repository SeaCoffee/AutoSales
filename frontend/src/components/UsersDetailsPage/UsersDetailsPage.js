import React, { useEffect, useState } from 'react';
import axios from 'axios';

const UserDetailsPage = () => {
  const [user, setUser] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    axios.get('/api/users/user/', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    })
    .then(response => {
      setUser(response.data);
    })
    .catch(error => {
      setError('Не удалось загрузить данные пользователя');
      console.error(error);
    });
  }, []);

  if (error) {
    return <div>{error}</div>;
  }

  if (!user) {
    return <div>Загрузка...</div>;
  }

  return (
    <div style={{
      padding: '20px',
      maxWidth: '400px',
      margin: 'auto',
      boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
      borderRadius: '8px',
      backgroundColor: '#fff'
    }}>
      <h5 style={{ borderBottom: '1px solid #ccc', paddingBottom: '10px' }}>User Info</h5>
      <p>Username: {user.username}</p>
      <p>Role: {user.role}</p>
      <p>Account type: {user.account_type}</p>
      {user.profile ? (
        <div>
          <p>Name: {user.profile.name}</p>
          <p>Surname: {user.profile.surname}</p>
          <p>City: {user.profile.city}</p>
          {user.profile.avatar && <img src={user.profile.avatar} alt="Аватар" style={{ width: '100px', height: '100px', borderRadius: '50%' }} />}
        </div>
      ) : (
        <p>Profile doesnt exist</p>
      )}
    </div>
  );
};


export default UserDetailsPage;
