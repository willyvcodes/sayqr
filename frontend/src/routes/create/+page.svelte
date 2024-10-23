<script>
	import { create_new_page } from '$lib/api.js';
	import { goto } from '$app/navigation';
	let content = '';
	let error = null;
	let successMessage = '';

	const handleSubmit = async () => {
		try {
			const response = await create_new_page(content);
			if (response.ok) {
				const result = await response.json();
				const id = result._id;
				goto(`/page/${id}`);
			} else {
				error = 'Error creating page';
			}
		} catch (err) {
			error = 'Network error or bad request';
		}
	};
</script>

<section class="min-h-screen flex flex-col justify-center items-center bg-surface-500 text-white">
	<div class="w-full max-w-md">
		<h1 class="text-3xl font-bold mb-4 text-center">Create Your Page</h1>
		<textarea
			bind:value={content}
			class="w-full p-4 text-black rounded-lg mb-4"
			rows="8"
			placeholder="Enter your text here..."
		></textarea>
		<button
			class="btn btn-primary bg-primary-500 hover:bg-primary-900 text-white px-6 py-3 rounded-lg shadow-lg w-full"
			on:click={handleSubmit}
		>
			Create Page
		</button>

		{#if error}
			<p style="color: red;">{error}</p>
		{/if}

		{#if successMessage}
			<p>{successMessage}</p>
		{/if}
	</div>
</section>
