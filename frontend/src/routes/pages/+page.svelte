<script>
	import { getModalStore } from '@skeletonlabs/skeleton';
	import { getToastStore } from '@skeletonlabs/skeleton';
	import { goto } from '$app/navigation';
	import { token } from '$lib/auth.js';
	import { onMount } from 'svelte';

	const modalStore = getModalStore();
	const toastStore = getToastStore();

	export let data;

	let pages = [];

	onMount(() => {
		if (!$token) {
			goto('/login');
		}
	});

	$: if (data?.pages) {
		pages = data.pages;
	}

	const deletePage = async (pageId) => {
		const confirmDelete = await modalStore.trigger({
			type: 'confirm',
			title: 'Delete Page',
			body: 'Are you sure you want to delete this page? This action cannot be undone.',
			buttonTextConfirm: 'Delete',
			buttonTextCancel: 'Cancel'
		});

		if (confirmDelete) {
			try {
				const response = await fetch(`/api/page/${pageId}`, {
					method: 'DELETE',
					headers: {
						Authorization: `Bearer ${localStorage.getItem('token')}`
					}
				});

				if (response.ok) {
					pages = pages.filter((page) => page._id !== pageId);
					toastStore.trigger({
						message: 'Page deleted!',
						background: 'variant-ghost-success',
						autohide: true,
						timeout: 3000
					});
				} else {
					const error = await response.json();
					modalStore.trigger({
						type: 'alert',
						title: 'Error',
						body: error.detail || 'Failed to delete page',
						buttonTextConfirm: 'Close'
					});
				}
			} catch (err) {
				modalStore.trigger({
					type: 'alert',
					title: 'Error',
					body: 'Error deleting page',
					buttonTextConfirm: 'Close'
				});
			}
		}
	};
</script>

<section class="min-h-screen bg-surface-900 p-6">
	<div class="max-w-4xl mx-auto">
		<div class="flex justify-between items-center mb-6">
			<h1 class="text-3xl font-semibold text-primary-400">My Pages</h1>
			<button
				on:click={() => goto('/create')}
				class="bg-primary-500 hover:bg-primary-600 text-white px-4 py-2 rounded"
			>
				Create New Page
			</button>
		</div>
		{#if pages.length === 0}
			<div class="text-center text-surface-400 py-8">
				<p class="text-lg">You haven't created any pages yet.</p>
				<button on:click={() => goto('/create')} class="text-primary-400 hover:underline mt-2">
					Create your first page
				</button>
			</div>
		{:else}
			<div class="grid gap-4">
				{#each pages as page}
					<div class="bg-surface-800 p-4 rounded-lg shadow-lg">
						<div class="flex justify-between items-start">
							<div class="flex-grow">
								<p class="text-primary-300 text-lg mb-2">{page.content}</p>
							</div>
							<div class="flex gap-2">
								<button
									on:click={() => goto(`/page/${page._id}`)}
									class="text-primary-300 hover:underline"
								>
									View
								</button>
								<button
									on:click={() => deletePage(page._id)}
									class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded"
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
