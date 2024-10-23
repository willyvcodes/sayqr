import { get_page_by_id } from '$lib/api.js'

export async function load({ params }) {
    const { id } = params;

    try {
        const response = await get_page_by_id(id);

        if (response.ok) {
            const pageData = await response.json();
            console.log(pageData)
            return { pageData };
        } else {
            return { error: 'Page not found' };
        }
    } catch (error) {
        return { error: 'Failed to fetch the page' };
    }
}

