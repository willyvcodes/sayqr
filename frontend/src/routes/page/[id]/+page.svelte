<script>
	import { goto } from '$app/navigation';
	import { update_page_by_id, update_qr_code_by_id } from '$lib/api';
	import QRCode from 'qrcode';

	export let data;

	let content = '';
	let qrCodeDataUrl = '';
	let pageUrl = '';
	let showQRCode = false;

	$: if (data?.pageData) {
		content = data.pageData.content || '';
		qrCodeDataUrl = data.pageData.qr_code || '';
		pageUrl = `https://sayqr.vercel.app/page/${data.pageData._id}`;
	}

	const generateQRCode = async () => {
		try {
			qrCodeDataUrl = await QRCode.toDataURL(pageUrl);
			await update_qr_code_by_id(qrCodeDataUrl, data.pageData._id);
		} catch (err) {
			console.error('Error generating QR code:', err);
		}
	};

	const toggleQRCode = (event) => {
		event.preventDefault();
		showQRCode = !showQRCode;
	};

	const updateContent = async () => {
		try {
			const response = await update_page_by_id(content, data.pageData.id);
			if (!response.ok) {
				console.error('Failed to update content');
			}
		} catch (err) {
			console.error('Error updating content:', err);
		}
	};
</script>

<section class="flex flex-col items-center justify-center min-h-screen bg-surface-500 p-6">
	<p
		class="text-white text-xl sm:text-3xl md:text-4xl lg:text-6xl font-light text-center leading-relaxed"
	>
		{content}
	</p>

	<div class="mt-auto flex justify-between w-full p-4">
		<button on:click={updateContent} class="text-blue-500 hover:underline text-base sm:text-2lg">
			Update Content
		</button>

		<button on:click={() => goto('/')} class="text-white text-base sm:text-2lg">Home</button>

		{#if qrCodeDataUrl}
			<button on:click={toggleQRCode} class="text-blue-500 hover:underline text-base sm:text-2lg">
				{#if showQRCode}
					Hide QR Code
				{:else}
					Show QR Code
				{/if}
			</button>
		{:else}
			<button on:click={generateQRCode} class="text-blue-500 hover:underline text-base sm:text-2lg">
				Create QR Code
			</button>
		{/if}
	</div>

	{#if showQRCode && qrCodeDataUrl}
		<div class="mt-6">
			<img src={qrCodeDataUrl} alt="QR Code" class="mx-auto" />
			<p class="text-gray-400 mt-2 text-center">Scan this code to visit the page.</p>
		</div>
	{/if}
</section>
