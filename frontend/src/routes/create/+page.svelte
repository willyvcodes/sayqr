<script>
	import { create_new_page } from '$lib/api.js';
	import { goto } from '$app/navigation';
	import { getToastStore } from '@skeletonlabs/skeleton';
	import { ProgressRadial } from '@skeletonlabs/skeleton';
	import { token } from '$lib/auth.js';
	import { onMount } from 'svelte';
	import ImageUploader from '$lib/components/ImageUploader.svelte';

	let content = '';
	let isLoading = false;
	let images = [];
	let imagePreviews = [];

	const toastStore = getToastStore();

	onMount(() => {
		if (!$token) {
			goto('/login');
		}
	});

	const handleImagesUploaded = (newImages) => {
		images = [...images, ...newImages];
		imagePreviews = [...imagePreviews, ...newImages];
	};

	const handleSubmit = async () => {
		if (!$token) {
			toastStore.trigger({
				message: 'Please log in to create a page',
				background: 'variant-ghost-error',
				autohide: true,
				timeout: 5000
			});
			goto('/login');
			return;
		}

		if (!content.trim()) {
			toastStore.trigger({
				message: 'Content cannot be empty',
				background: 'variant-ghost-error',
				autohide: true,
				timeout: 5000
			});
			return;
		}

		isLoading = true;

		try {
			const response = await create_new_page(content, images);
			if (response.ok) {
				const page = await response.json();
				console.log('Page created:', page._id);
				goto(`/page/${page._id}`);
			} else {
				toastStore.trigger({
					message: 'Error creating page',
					background: 'variant-ghost-error',
					autohide: true,
					timeout: 5000
				});
			}
		} catch (err) {
			toastStore.trigger({
				message: 'Network error or bad request',
				background: 'variant-ghost-error',
				autohide: true,
				timeout: 5000
			});
		} finally {
			isLoading = false;
		}
	};
</script>

<section
	class="min-h-screen flex flex-col justify-center items-center bg-surface-900 text-white px-4"
>
	<div class="w-full max-w-md space-y-6 bg-surface-700 p-8 rounded-lg shadow-lg">
		<h1 class="text-3xl font-semibold mb-6 text-center tracking-tight text-primary-400">
			Create Your Page
		</h1>
		<textarea
			bind:value={content}
			class="w-full p-4 text-white rounded-lg mb-6 shadow-inner border border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-600 bg-surface-800 placeholder-gray-400"
			rows="8"
			placeholder="Enter your text here..."
		></textarea>
		<ImageUploader onImagesUploaded={handleImagesUploaded} disabled={isLoading} />
		{#if imagePreviews.length}
			<div class="flex flex-wrap gap-2 mb-4">
				{#each imagePreviews as img}
					<img
						src={img}
						alt="Preview"
						class="w-20 h-20 object-cover rounded border border-primary-500"
					/>
				{/each}
			</div>
		{/if}
		<button
			class="btn btn-primary bg-primary-500 hover:bg-primary-600 text-white py-3 px-8 rounded-md shadow-lg transition-transform transform hover:scale-105 w-full"
			on:click={handleSubmit}
			disabled={isLoading}
		>
			Create Page
		</button>
	</div>
	{#if isLoading}
		<div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
			<ProgressRadial value={undefined} width="w-10 h-10" />
		</div>
	{/if}
</section>
