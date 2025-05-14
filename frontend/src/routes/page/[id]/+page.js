import { get_page_by_id } from '$lib/api.js';

export async function load({ params }) {
    const { id } = params;
    const response = await get_page_by_id(id);

    if (response.ok) {
        const pageData = await response.json();
        return { pageData };
    } else {
        return { pageData: { content: 'Page not found.' } };
    }
}
