import React, { useEffect, useState } from 'react';
import axios from 'axios';

const ProfileDetail = () => {
    const [profile, setProfile] = useState(null);
    const [error, setError] = useState('');

    useEffect(() => {
    const fetchProfile = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.get('/api/users/profile/', {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            if (response.data && Object.keys(response.data).length > 0) {
                setProfile(response.data);
                console.log(response.data);  // Проверяем, что приходит в ответе
            } else {
                setError('Profile data is empty.');
            }
        } catch (err) {
            console.error(err);
            if (err.response && err.response.status === 404) {
                setError('Profile not found. Please complete your profile.');
            } else {
                setError('Failed to fetch profile. ' + err.message);
            }
        }
    };

    fetchProfile();
}, []);


    const containerStyle = {
        maxWidth: '400px',
        margin: '0 auto',
        padding: '20px',
        border: '1px solid #ccc',
        borderRadius: '8px',
        backgroundColor: '#f9f9f9',
        textAlign: 'center',
    };

    const headingStyle = {
        marginBottom: '20px',
        fontSize: '24px',
        color: '#333',
    };

    const avatarStyle = {
        width: '150px',
        height: '150px',
        borderRadius: '50%',
        marginBottom: '20px',
    };

    const textStyle = {
        marginBottom: '10px',
        fontSize: '16px',
        color: '#555',
    };

    const errorStyle = {
        color: 'red',
        fontSize: '16px',
        marginTop: '20px',
    };

    if (error) {
        return <div style={errorStyle}>Error: {error}</div>;
    }

    if (!profile) {
        return <div style={textStyle}>Loading profile...</div>;
    }

    return (
        <div style={containerStyle}>
            <h1 style={headingStyle}>User Profile</h1>
            {profile.avatar ? (
                <img
                    src={profile.avatar}
                    alt={`${profile.name || 'User'}'s avatar`}
                    style={avatarStyle}
                />
            ) : (
                <p style={textStyle}>No avatar available</p>
            )}
            <p style={textStyle}>Name: {profile.name ? profile.name : 'Name not provided'}</p>
            <p style={textStyle}>Email: {profile.email ? profile.email : 'Email not provided'}</p>
            <p style={textStyle}>Account Type: {profile.account_type ? profile.account_type : 'Account type not provided'}</p>
        </div>
    );
};

export default ProfileDetail;

