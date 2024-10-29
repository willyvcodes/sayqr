<script>
	import '../app.postcss';

	import { initializeStores, Toast, Modal } from '@skeletonlabs/skeleton';
	initializeStores();
</script>

<Toast />
<Modal />
<slot />
