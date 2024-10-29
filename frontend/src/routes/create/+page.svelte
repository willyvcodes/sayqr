<script>
	import { create_new_page } from '$lib/api.js';
	import { goto } from '$app/navigation';
	import { getToastStore } from '@skeletonlabs/skeleton';
	import { ProgressRadial } from '@skeletonlabs/skeleton';

	const toastStore = getToastStore();

	let content = '';
	let isLoading = false;

	const handleSubmit = async () => {
		if (!content.trim()) {
			showErrorToast('Content cannot be empty');
			return;
		}

		isLoading = true;

		try {
			const response = await create_new_page(content);
			if (response.ok) {
				const result = await response.json();
				const id = result._id;
				goto(`/page/${id}`);
			} else {
				showErrorToast('Error creating page');
			}
		} catch (err) {
			showErrorToast('Network error or bad request');
		} finally {
			isLoading = false;
		}
	};

	const showErrorToast = (message) => {
		const toastSettings = {
			message,
			background: 'variant-ghost-warning',
			autohide: true,
			timeout: 5000
		};
		toastStore.trigger(toastSettings);
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
