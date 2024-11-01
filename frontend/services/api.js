import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001/api', // Use Django backend URL
});

export const getInventoryItems = async () => {
  try {
    const response = await api.get('/inventory-list/');
    return response.data;
  } catch (error) {
    console.error('Error fetching inventory items:', error);
    throw error;
  }
};

export const getPatientDetails = async (patientId) => {
  try {
    const response = await api.get(`/patients/${patientId}/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching patient details:', error);
    throw error;
  }
};
