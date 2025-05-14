import { error } from '@sveltejs/kit';

export async function load({ fetch, cookies }) {
    const token = cookies.get('token');
    if (!token) {
        throw error(401, 'Not authenticated');
    }

    try {
        const response = await fetch('/api/pages/my', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw error(response.status, 'Failed to fetch pages');
        }

        const pages = await response.json();
        return { pages };
    } catch (err) {
        throw error(500, 'Error fetching pages');
    }
} 