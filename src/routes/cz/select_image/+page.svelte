<script lang="ts">
	import { convertFileSrc, invoke } from '@tauri-apps/api/tauri';
	import { open } from '@tauri-apps/api/dialog';
	import { homeDir } from '@tauri-apps/api/path';
	import { onMount } from 'svelte';

	let homeDirPath = '';
    let imageUrl = '';
	let origImagePath = '';

    // Use onMount with an async function to perform async operations
    onMount(async () => {
        // Await the homeDir call!!!
        homeDirPath = await homeDir();
        const basePath = `${homeDirPath}.local/share/stamp-guard/frontend`;
        origImagePath = `${basePath}/orig_image.jpg`;

		// Convert the file path to a URL that can be used in an img tag
        imageUrl = `${convertFileSrc(origImagePath)}?t=${new Date().getTime()}`;
		console.log("Image URL set on page load:", imageUrl);
    });

    async function handleFileSelection() {
		console.log("Starting handleFileSelection")
        const selectedFilePath = await open({
            multiple: false,
            directory: false,
            title: "Select an image"
        });

        if (selectedFilePath) {
			await invoke('save_image', { message: selectedFilePath });
			await new Promise(resolve => setTimeout(resolve, 2000));
			console.log("Done invoking save_image")

            // Cache busting: Add a unique query parameter to the image URL
            imageUrl = `${convertFileSrc(origImagePath)}?t=${new Date().getTime()}`;
			console.log("Done Async handleFileSelection")
        }
    }

    function handleNavigation() {
        window.location.href = '/cz/display_image';
    }
</script>

<style>
    :global(body, html) {
        margin: 0;
	    overflow: hidden;
	    height: 100vh;
		width: 100vw;
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

    #re-selectButton {
        background-color: #f00;
        color: #fff;
        border-color: #f00;
    }

    #re-selectButton:hover {
        background-color: #fff;
        color: #f00;
    }
</style>

<main>
	<div class="container">
        <div class="image-button-wrapper">
            <img id="selectedImage" src={imageUrl} alt="User Selected"/>
            <div class="button-row">
                <button id="ConfirmButton" on:click={handleNavigation}>Potvrdit</button>
                <button id="re-selectButton" on:click={handleFileSelection}>Vybrat znovu</button>
            </div>
        </div>
    </div>
</main>
