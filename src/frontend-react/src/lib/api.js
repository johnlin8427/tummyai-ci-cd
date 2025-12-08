import axios from 'axios';

const apiClient = axios.create({
    baseURL: process.env.NEXT_PUBLIC_BASE_API_URL || 'http://localhost:9000',
    headers: {
        'Content-Type': 'application/json',
    },
});

export default apiClient;
