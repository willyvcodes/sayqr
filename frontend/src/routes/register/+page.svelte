<script>
	import { register } from '$lib/api.js';
	import { goto } from '$app/navigation';
	import { getToastStore } from '@skeletonlabs/skeleton';

	let email = '';
	let password = '';
	let error = '';
	let success = '';

	const toastStore = getToastStore();

	const handleRegister = async () => {
		error = '';
		success = '';
		const response = await register(email, password);
		if (response.ok) {
			success = 'Registration successful! You can now log in.';
			toastStore.trigger({
				message: 'Registration successful! You can now log in.',
				background: 'variant-ghost-success',
				autohide: true,
				timeout: 5000
			});
			setTimeout(() => goto('/login'), 1500);
		} else {
			const data = await response.json();
			toastStore.trigger({
				message: data.detail || 'Registration failed',
				background: 'variant-ghost-error',
				autohide: true,
				timeout: 5000
			});
			error = data.detail || 'Registration failed';
		}
	};
</script>

<div class="max-w-md mx-auto mt-16 p-8 bg-surface-700 rounded-lg shadow-lg">
	<h1 class="text-2xl font-bold mb-6 text-center">Register</h1>
	<input class="w-full mb-4 p-2 rounded" type="email" placeholder="Email" bind:value={email} />
	<input
		class="w-full mb-4 p-2 rounded"
		type="password"
		placeholder="Password"
		bind:value={password}
	/>
	{#if error}
		<div class="text-red-500 mb-4">{error}</div>
	{/if}
	{#if success}
		<div class="text-green-500 mb-4">{success}</div>
	{/if}
	<button class="btn btn-primary w-full" on:click={handleRegister}>Register</button>
	<div class="mt-4 text-center">
		<a href="/login" class="text-primary-400 hover:underline">Already have an account? Login</a>
	</div>
</div>
