import axios from 'axios';
import { BASE_API_URL } from './Common';

const apiClient = axios.create({
    baseURL: BASE_API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export default apiClient;
