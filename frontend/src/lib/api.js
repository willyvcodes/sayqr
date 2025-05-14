import { get } from 'svelte/store';
import { token } from './auth.js';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const getAuthHeaders = () => {
    const t = get(token);
    return t
        ? { 'Content-Type': 'application/json', Authorization: `Bearer ${t}` }
        : { 'Content-Type': 'application/json' };
};

// Create a new page with initial content and images
export const create_new_page = async (content, images = []) => {
    return await fetch(`${API_BASE_URL}/api/page/`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ content, images })
    });
};

// Get page by ID
export const get_page_by_id = async (page_id) => {
    return await fetch(`${API_BASE_URL}/api/page/${page_id}`, {
        method: 'GET',
        headers: getAuthHeaders()
    });
};

// Update page content and images by ID
export const update_page_by_id = async (page_id, { content, images }) => {
    return await fetch(`${API_BASE_URL}/api/page/${page_id}`, {
        method: 'PUT',
        headers: getAuthHeaders(),
        body: JSON.stringify({ content, images })
    });
};

// Login (returns JWT)
export const login = async (email, password) => {
    return await fetch(`${API_BASE_URL}/auth/jwt/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ username: email, password })
    });
};

// Register
export const register = async (email, password) => {
    return await fetch(`${API_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });
};

// Get all pages for the current user
export const get_my_pages = async () => {
    return await fetch(`${API_BASE_URL}/api/pages/my`, {
        method: 'GET',
        headers: getAuthHeaders()
    });
};

// Delete a page by ID
export const delete_page = async (page_id) => {
    return await fetch(`${API_BASE_URL}/api/page/${page_id}`, {
        method: 'DELETE',
        headers: getAuthHeaders()
    });
};
