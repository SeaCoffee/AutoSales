import React, { useState } from 'react';
import axios from 'axios';

const UserCreate = () => {
    const [userData, setUserData] = useState({ email: '', password: '', username: '' });
    const [message, setMessage] = useState('');

    const handleChange = (e) => {
        setUserData({ ...userData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            await axios.post('api/users/', userData);
            setMessage('User created successfully.');
        } catch (error) {
            setMessage('Failed to create user.');
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input type="email" name="email" value={userData.email} onChange={handleChange} placeholder="Email" />
                <input type="password" name="password" value={userData.password} onChange={handleChange} placeholder="Password" />
                <input type="text" name="username" value={userData.username} onChange={handleChange} placeholder="Username" />
                <button type="submit">Create User</button>
            </form>
            {message}
        </div>
    );
};

export default UserCreate;
