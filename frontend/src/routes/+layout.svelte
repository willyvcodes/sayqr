<script>
	import '../app.postcss';

	import { initializeStores, Toast, Modal } from '@skeletonlabs/skeleton';
	initializeStores();

	import { token } from '$lib/auth.js';
	import { goto } from '$app/navigation';

	function logout() {
		token.set(null);
		goto('/login');
	}
</script>

<Toast />
<Modal />

<nav class="bg-surface-800 p-4">
	<div class="container mx-auto flex justify-between items-center">
		<a href="/" class="text-xl font-bold text-primary-400">SayQR</a>
		<div class="space-x-4">
			{#if $token}
				<a href="/my-pages" class="btn btn-secondary">My Pages</a>
				<button class="btn btn-primary" on:click={logout}>Logout</button>
			{:else}
				<a href="/login" class="btn btn-primary">Login</a>
				<a href="/register" class="btn btn-secondary">Register</a>
			{/if}
		</div>
	</div>
</nav>

<main class="container mx-auto p-4">
	<slot />
</main>
