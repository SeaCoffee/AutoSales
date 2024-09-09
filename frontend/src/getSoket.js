import axios from 'axios';

const getSocketToken = async () => {
    try {
        const response = await axios.get('api/auth/soket/');
        console.log('Socket token received:', response.data.token);
        return response.data.token;
    } catch (error) {
        console.error('Failed to get socket token:', error);
        return null;
    }
};
