import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function RegistrationPage() {
    const [formData, setFormData] = useState({
        email: '',
        username: '',
        password: '',
        name: '',
        surname: '',
        age: '',
        city: '',
        roleId: '',
    });

    const [roles, setRoles] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchRoles = async () => {
            try {
                const response = await axios.get('/api/auth/roles/');
                setRoles(response.data.data);
            } catch (error) {
                console.error('Failed to fetch roles', error);
            }
        };
        fetchRoles();
    }, []);

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.name === 'roleId' ? parseInt(e.target.value) : e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        const profileData = {
            name: formData.name,
            surname: formData.surname,
            age: formData.age,
            city: formData.city,
        };

        const user = {
            email: formData.email,
            username: formData.username,
            password: formData.password,
            role: formData.roleId,
            profile: profileData,
        };

        try {
            const response = await axios.post('/api/users/', user);
            console.log('Registration successful', response.data);
            setFormData({
                email: '',
                username: '',
                password: '',
                name: '',
                surname: '',
                age: '',
                city: '',
                roleId: '',
            });
            navigate('/logIn');
        } catch (error) {
            console.error('Registration error', error.response.data);
        }
    };

    // Стилизация прямо в компоненте
    const formStyle = {
        display: 'flex',
        flexDirection: 'column',
        maxWidth: '400px',
        margin: '0 auto',
        padding: '20px',
        border: '1px solid #ccc',
        borderRadius: '8px',
        backgroundColor: '#f9f9f9',
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

    const buttonHoverStyle = {
        backgroundColor: '#45a049',
    };

    return (
        <form onSubmit={handleSubmit} style={formStyle}>
            <input type="email" name="email" placeholder="Email" onChange={handleChange} required style={inputStyle} />
            <input type="text" name="username" placeholder="Username" onChange={handleChange} required style={inputStyle} />
            <input type="password" name="password" placeholder="Password" onChange={handleChange} required style={inputStyle} />
            <input type="text" name="name" placeholder="Name" onChange={handleChange} style={inputStyle} />
            <input type="text" name="surname" placeholder="Surname" onChange={handleChange} style={inputStyle} />
            <input type="number" name="age" placeholder="Age" onChange={handleChange} style={inputStyle} />
            <input type="text" name="city" placeholder="City" onChange={handleChange} style={inputStyle} />
            <select name="roleId" onChange={handleChange} value={formData.roleId} required style={inputStyle}>
                <option value="">Select Role</option>
                {Array.isArray(roles) ? roles.map(role => (
                    <option key={role.id} value={role.id}>{role.name}</option>
                )) : <option disabled>Loading roles...</option>}
            </select>

            <button type="submit" style={{ ...buttonStyle, ':hover': buttonHoverStyle }}>Register</button>
        </form>
    );
}

export default RegistrationPage;


