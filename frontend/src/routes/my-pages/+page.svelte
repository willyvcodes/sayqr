<script>
	import { get_my_pages, delete_page } from '$lib/api.js';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { getToastStore } from '@skeletonlabs/skeleton';
	import { ProgressRadial } from '@skeletonlabs/skeleton';
	import { token } from '$lib/auth.js';

	let pages = [];
	let isLoading = true;
	let error = null;

	const toastStore = getToastStore();

	onMount(async () => {
		if (!$token) {
			goto('/login');
			return;
		}
		try {
			const response = await get_my_pages();
			if (response.ok) {
				pages = await response.json();
			} else {
				error = 'Failed to load pages';
			}
		} catch (err) {
			error = 'Network error';
		} finally {
			isLoading = false;
		}
	});

	const formatDate = (dateString) => {
		return new Date(dateString).toLocaleDateString('en-US', {
			year: 'numeric',
			month: 'short',
			day: 'numeric'
		});
	};

	const deletePage = async (pageId) => {
		if (!$token) {
			toastStore.trigger({
				message: 'Please log in to delete pages',
				background: 'variant-ghost-warning',
				autohide: true,
				timeout: 5000
			});
			goto('/login');
			return;
		}

		if (!confirm('Are you sure you want to delete this page? This action cannot be undone.')) {
			return;
		}

		try {
			const response = await delete_page(pageId);
			if (response.ok) {
				pages = pages.filter((page) => page._id !== pageId);
				toastStore.trigger({
					message: 'Page deleted successfully',
					background: 'variant-ghost-success',
					autohide: true,
					timeout: 5000
				});
			} else {
				const error = await response.json();
				toastStore.trigger({
					message: error.detail || 'Failed to delete page',
					background: 'variant-ghost-warning',
					autohide: true,
					timeout: 5000
				});
			}
		} catch (err) {
			toastStore.trigger({
				message: 'Error deleting page',
				background: 'variant-ghost-warning',
				autohide: true,
				timeout: 5000
			});
		}
	};
</script>

<section class="min-h-screen bg-surface-900 p-6">
	<div class="container mx-auto">
		<div class="flex justify-between items-center mb-8">
			<h1 class="text-3xl font-bold text-primary-400">My Pages</h1>
			<a
				href="/create"
				class="btn btn-primary bg-primary-500 hover:bg-primary-600 text-white py-2 px-4 rounded-md shadow-md transition-transform transform hover:scale-105"
			>
				Create New Page
			</a>
		</div>

		{#if isLoading}
			<div class="flex justify-center items-center h-64">
				<ProgressRadial value={undefined} width="w-10 h-10" />
			</div>
		{:else if error}
			<div class="text-center text-red-500 p-4">{error}</div>
		{:else if pages.length === 0}
			<div class="text-center text-surface-400 py-8">
				<p class="text-lg">You haven't created any pages yet.</p>
				<button
					type="button"
					on:click={() => goto('/create')}
					class="text-primary-400 hover:underline mt-2"
				>
					Create your first page
				</button>
			</div>
		{:else}
			<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
				{#each pages as page}
					<div class="bg-surface-800 rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow">
						{#if page.images && page.images.length > 0}
							<img
								src={page.images[0]}
								alt="Page preview"
								class="w-full h-48 object-cover rounded-lg mb-4"
							/>
						{/if}
						<p class="text-primary-300 text-lg mb-2 line-clamp-3">{page.content}</p>
						<div class="flex justify-between items-center text-sm text-gray-400">
							<span>Created: {formatDate(page.created_at)}</span>
							<div class="flex gap-2">
								<button
									type="button"
									class="text-primary-400 hover:text-primary-300"
									on:click={() => goto(`/page/${page._id}`)}
								>
									View
								</button>
								<button
									type="button"
									class="text-red-500 hover:text-red-400"
									on:click={() => deletePage(page._id)}
								>
									Delete
								</button>
							</div>
						</div>
					</div>
				{/each}
			</div>
		{/if}
	</div>
</section>
