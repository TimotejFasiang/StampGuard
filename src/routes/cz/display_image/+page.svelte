<script lang="ts">
	import { onMount } from 'svelte';
	import { homeDir } from '@tauri-apps/api/path';
	import { convertFileSrc } from '@tauri-apps/api/tauri';
	import { appWindow } from '@tauri-apps/api/window';

	let showButtonRow: boolean = false;
	let imageUrl: string;

	async function loadImage() {
		const homeDirPath = await homeDir();
		const basePath = `${homeDirPath}.local/share/stamp-guard/frontend`;
		const processedImagePath = `${basePath}/processed_image.jpg`;
		imageUrl = convertFileSrc(processedImagePath);
		showButtonRow = true; // Show the button row once the image is loaded
	}

	function navigateBack() {
		window.location.href = '/en/select_image';
	}

	function exitApp() {
		appWindow.close();
	}

	onMount(loadImage);
</script>

<style>
    :global(body, html) {
        margin: 0;
	    overflow: hidden;
    }

	.container {
		display: flex;
		justify-content: center;
		align-items: center;
		height: 100vh;
		width: 100vw;
		overflow: hidden;
	}

    .image-button-wrapper {
        display: flex;
	    flex-direction: column;
        justify-content: center;
        align-items: center;
	    overflow: hidden;
    }

    img {
	    max-height: calc(90vh - 55px);
        max-width: 90vw;
        width: auto;
        height: auto;
        border: 5px solid black;
        border-radius: 3px;
        box-sizing: border-box;
    }

    .button-row {
        display: flex;
	    padding-top: 10px;
	    width: 100%;
        justify-content: space-between;
	    box-sizing: border-box;
    }

    button {
        padding: 10px 24px;
        font-size: 18px;
	    border-radius: 3px;
        cursor: pointer;
	    background-color: #000;
        color: #fff;
	    border: 2px solid #000;
    }

    button:hover {
	    background-color: #fff;
        color: #000;
    }

    #exitButton {
        background-color: #f00;
        color: #fff;
        border-color: #f00;
    }

    #exitButton:hover {
        background-color: #fff;
        color: #f00;
    }
</style>

<main>
	<div class="container">
		<div class="image-button-wrapper">
			{#if imageUrl}
				<img id="selectedImage" src={imageUrl} alt="Processed image" />
			{/if}
			{#if showButtonRow}
				<div class="button-row">
					<button id="backButton" on:click={navigateBack}>Zpět</button>
					<button id="exitButton" on:click={exitApp}>Hotovo</button>
				</div>
			{/if}
		</div>
	</div>
</main>
