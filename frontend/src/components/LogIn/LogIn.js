import React, {useEffect, useState} from 'react';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';
import { useNavigate } from 'react-router-dom';


const LogIn = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (token) {
            try {
                const decodedToken = jwtDecode(token);
                console.log('Token decoded:', decodedToken);
            } catch (err) {
                console.error('Failed to decode token:', err);
                localStorage.removeItem('token');
                navigate('/login');
            }
        }
    }, [navigate]);

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            console.log('URL before request:', axios.defaults.baseURL);
            const response = await axios.post('/api/auth/', { username, password });

            const { access } = response.data;
            localStorage.setItem('token', access);
            console.log('Token saved:', access);

            setUsername('');
            setPassword('');

            navigate('/');
        } catch (err) {
            console.error('Login Error:', err.response || err.message);
            setError('Ошибка входа: ' + (err.response?.data?.detail || err.message));
        }
    };


    const formStyle = {
        display: 'flex',
        flexDirection: 'column',
        maxWidth: '300px',
        margin: '0 auto',
        padding: '20px',
        border: '1px solid #ccc',
        borderRadius: '8px',
        backgroundColor: '#f9f9f9',
    };

    const labelStyle = {
        marginBottom: '10px',
        fontSize: '14px',
    };

    const inputStyle = {
        marginBottom: '10px',
        padding: '8px',
        fontSize: '16px',
        borderRadius: '4px',
        border: '1px solid #ccc',
    };

    const buttonStyle = {
        padding: '10px',
        fontSize: '16px',
        backgroundColor: '#4CAF50',
        color: 'white',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
    };

    const errorStyle = {
        color: 'red',
        marginTop: '10px',
    };

    return (
        <form onSubmit={handleSubmit} style={formStyle}>
            <label style={labelStyle}>
                Логин:
                <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    style={inputStyle}
                    required
                />
            </label>
            <label style={labelStyle}>
                Пароль:
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    style={inputStyle}
                    required
                />
            </label>
            <button type="submit" style={buttonStyle}>Войти</button>
            {error && <p style={errorStyle}>{error}</p>}
        </form>
    );
};

export default LogIn;