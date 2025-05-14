import { writable } from 'svelte/store';
import { browser } from '$app/environment';

export const token = writable(
    browser ? localStorage.getItem('token') : null
);

token.subscribe((value) => {
    if (browser) {
        if (value) {
            localStorage.setItem('token', value);
        } else {
            localStorage.removeItem('token');
        }
    }
});
