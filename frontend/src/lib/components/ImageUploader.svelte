<script>
	import imageCompression from 'browser-image-compression';
	import { getToastStore } from '@skeletonlabs/skeleton';

	const toastStore = getToastStore();

	export let onImagesUploaded = () => {};
	export let disabled = false;

	let isUploading = false;

	const handleImageChange = async (event) => {
		const files = Array.from(event.target.files);
		const compressedImages = [];

		isUploading = true;
		try {
			for (const file of files) {
				const options = {
					maxSizeMB: 0.3,
					maxWidthOrHeight: 1200,
					useWebWorker: true
				};
				const compressedFile = await imageCompression(file, options);
				const base64 = await imageCompression.getDataUrlFromFile(compressedFile);
				compressedImages.push(base64);
			}

			onImagesUploaded(compressedImages);
		} catch (err) {
			showErrorToast('Error processing images: ' + err.message);
		} finally {
			isUploading = false;
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

<div class="w-full">
	<input
		type="file"
		accept="image/*"
		multiple
		on:change={handleImageChange}
		class="block w-full text-white mb-2"
		disabled={disabled || isUploading}
	/>
	{#if isUploading}
		<div class="text-primary-400 text-center">Uploading images...</div>
	{/if}
</div>
