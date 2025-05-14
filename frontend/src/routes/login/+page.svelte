<script>
	import { login } from '$lib/api.js';
	import { token } from '$lib/auth.js';
	import { goto } from '$app/navigation';
	import { getToastStore } from '@skeletonlabs/skeleton';

	let email = '';
	let password = '';
	let error = '';

	const toastStore = getToastStore();

	const handleLogin = async () => {
		error = '';
		const response = await login(email, password);
		if (response.ok) {
			const data = await response.json();
			token.set(data.access_token);
			goto('/');
		} else {
			toastStore.trigger({
				message: 'Invalid email or password',
				background: 'variant-ghost-error',
				autohide: true,
				timeout: 5000
			});
			error = 'Invalid email or password';
		}
	};
</script>

<div class="max-w-md mx-auto mt-16 p-8 bg-surface-700 rounded-lg shadow-lg">
	<h1 class="text-2xl font-bold mb-6 text-center">Login</h1>
	<input
		class="w-full mb-4 p-2 rounded bg-surface-800 text-white placeholder-gray-400 border border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-600"
		type="email"
		placeholder="Email"
		bind:value={email}
	/>
	<input
		class="w-full mb-4 p-2 rounded bg-surface-800 text-white placeholder-gray-400 border border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-600"
		type="password"
		placeholder="Password"
		bind:value={password}
	/>
	{#if error}
		<div class="text-red-500 mb-4">{error}</div>
	{/if}
	<button class="btn btn-primary w-full" on:click={handleLogin}>Login</button>
	<div class="mt-4 text-center">
		<a href="/register" class="text-primary-400 hover:underline">Don't have an account? Register</a>
	</div>
</div>
