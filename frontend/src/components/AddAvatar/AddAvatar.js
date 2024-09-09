import React, { useState } from 'react';
import axios from 'axios';

const AddAvatar = () => {
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        const formData = new FormData();
        formData.append('avatar', file);


        try {
            const response = await axios.put('api/users/avatars/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            setMessage('Avatar updated successfully.');
        } catch (error) {
            setMessage('Failed to update avatar.');
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input type="file" onChange={(e) => setFile(e.target.files[0])} />
                <button type="submit">Upload Avatar</button>
            </form>
            {message}
        </div>
    );
};

export default AddAvatar;
