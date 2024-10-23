const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;


const headers = {
    'Content-Type': 'application/json'
};

// Create a new page with initial content
export const create_new_page = async (content) => {
    return await fetch(`${API_BASE_URL}/api/page/`, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({ content })
    });
};

// Get page by ID
export const get_page_by_id = async (page_id) => {
    return await fetch(`${API_BASE_URL}/api/page/` + page_id, {
        method: 'GET',
        headers: headers
    });
};

// Update page content by ID
export const update_page_by_id = async (content, page_id) => {
    return await fetch(`${API_BASE_URL}/api/page/` + page_id + '/content', {
        method: 'PUT',
        headers: headers,
        body: JSON.stringify({ content })
    });
};

// Update QR code by page ID
export const update_qr_code_by_id = async (qr_code, page_id) => {
    return await fetch(`${API_BASE_URL}/api/page/` + page_id + '/qr_code', {
        method: 'PUT',
        headers: headers,
        body: JSON.stringify(qr_code)
    });
};
