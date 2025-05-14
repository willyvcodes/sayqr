<script>
	import { get_page_by_id, update_page_by_id } from '$lib/api';
	import { goto } from '$app/navigation';
	import QRCode from 'qrcode';
	import { getModalStore } from '@skeletonlabs/skeleton';
	import { browser } from '$app/environment';
	import { token } from '$lib/auth.js';

	const modalStore = getModalStore();

	export let data;

	let content = '';
	let qrCodeDataUrl = '';
	let pageUrl = '';
	let images = [];
	let isOwner = false;

	$: if (data?.pageData) {
		content = data.pageData.content || '';
		images = data.pageData.images || [];
		if (browser) {
			pageUrl = `${window.location.origin}/page/${data.pageData._id}`;
			const currentToken = localStorage.getItem('token');
			if (currentToken) {
				const payload = JSON.parse(atob(currentToken.split('.')[1]));
				isOwner = payload.sub === data.pageData.user_id;
			}
		}
	}

	const generateQRCode = async () => {
		try {
			qrCodeDataUrl = await QRCode.toDataURL(pageUrl);
		} catch (err) {
			modalStore.trigger({
				type: 'alert',
				title: 'Error',
				body: 'Error generating QR code',
				buttonTextConfirm: 'Close'
			});
		}
	};

	const showQRCodeModal = async () => {
		if (!qrCodeDataUrl) {
			await generateQRCode();
		}
		const qrCodeModalSettings = {
			type: 'alert',
			title: 'QR Code',
			body: `<img src="${qrCodeDataUrl}" alt="QR Code" class="w-40 h-40 mb-4 mx-auto" />`,
			backdropClasses: 'bg-black bg-opacity-50',
			modalClasses: 'bg-surface-800 p-6 rounded-lg shadow-lg text-center',
			buttonTextConfirm: 'Close'
		};
		modalStore.trigger(qrCodeModalSettings);
	};

	const showEditContentModal = () => {
		if (!isOwner) {
			modalStore.trigger({
				type: 'alert',
				title: 'Access Denied',
				body: 'You do not have permission to edit this page.',
				buttonTextConfirm: 'Close'
			});
			return;
		}

		const editContentModalSettings = {
			type: 'prompt',
			title: 'Edit Content',
			body: 'Provide new content for the page:',
			value: content,
			backdropClasses: 'bg-black bg-opacity-50',
			modalClasses: 'bg-surface-800 p-6 rounded-lg shadow-lg text-center',
			buttonTextConfirm: 'Save',
			buttonTextCancel: 'Cancel',
			response: async (newContent) => {
				if (newContent && newContent !== content) {
					try {
						const updateResponse = await update_page_by_id(data.pageData._id, {
							content: newContent
						});
						if (updateResponse.ok) {
							content = newContent;
						} else {
							modalStore.trigger({
								type: 'alert',
								title: 'Error',
								body: 'Failed to update content',
								buttonTextConfirm: 'Close'
							});
						}
					} catch (err) {
						modalStore.trigger({
							type: 'alert',
							title: 'Error',
							body: 'Error updating content',
							buttonTextConfirm: 'Close'
						});
					}
				}
			}
		};
		modalStore.trigger(editContentModalSettings);
	};
</script>

<section class="min-h-screen flex flex-col justify-between bg-surface-900 p-6">
	<div class="flex-grow flex flex-col items-center justify-center">
		{#if images.length}
			<div class="flex flex-wrap gap-4 mb-6 justify-center">
				{#each images as img}
					<img src={img} alt="" class="w-40 h-40 object-cover rounded border border-primary-500" />
				{/each}
			</div>
		{/if}
		<p class="text-5xl font-light text-primary-300 text-center leading-relaxed">
			{content}
		</p>
	</div>
	<div class="flex justify-between items-center mt-8 w-full max-w-3xl mx-auto">
		<button on:click={() => goto('/')} class="text-primary-300 hover:underline"> Home </button>
		<button on:click={showQRCodeModal} class="text-primary-300 hover:underline">
			Show QR Code
		</button>
		{#if isOwner}
			<button on:click={showEditContentModal} class="text-primary-300 hover:underline">
				Edit Content
			</button>
		{/if}
	</div>
</section>
