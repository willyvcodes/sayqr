<script>
	import { get_page_by_id, update_page_by_id } from '$lib/api';
	import { goto } from '$app/navigation';
	import QRCode from 'qrcode';
	import { getModalStore } from '@skeletonlabs/skeleton';
	import { browser } from '$app/environment';

	const modalStore = getModalStore();

	export let data;

	let content = '';
	let qrCodeDataUrl = '';
	let pageUrl = '';

	$: if (data?.pageData) {
		content = data.pageData.content || '';
		if (browser) {
			pageUrl = `${window.location.origin}/page/${data.pageData._id}`;
		}
	}

	const generateQRCode = async () => {
		try {
			qrCodeDataUrl = await QRCode.toDataURL(pageUrl);
			console.log('Generated QR Code Data URL:', qrCodeDataUrl);
		} catch (err) {
			console.error('Error generating QR code:', err);
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
							console.log('Content updated successfully');
						} else {
							console.error(
								'Error updating content:',
								updateResponse.status,
								updateResponse.statusText
							);
						}
					} catch (err) {
						console.error('Error updating content:', err);
					}
				}
			}
		};
		modalStore.trigger(editContentModalSettings);
	};
</script>

<section class="min-h-screen flex flex-col justify-between bg-surface-900 p-6">
	<div class="flex-grow flex items-center justify-center">
		<p class="text-5xl font-light text-primary-300 text-center leading-relaxed">
			{content}
		</p>
	</div>
	<div class="flex justify-between items-center mt-8 w-full max-w-3xl mx-auto">
		<button on:click={() => goto('/')} class="text-primary-300 hover:underline"> Home </button>
		<button on:click={showQRCodeModal} class="text-primary-300 hover:underline">
			Show QR Code
		</button>
		<button on:click={showEditContentModal} class="text-primary-300 hover:underline">
			Edit Content
		</button>
	</div>
</section>
