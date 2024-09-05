<script lang="ts">
    import { invoke } from '@tauri-apps/api/tauri';
    import { open } from '@tauri-apps/api/dialog';

    // Function to handle file selection and invoke the command
    async function handleFileSelection() {
        console.log("Starting handleFileSelection")
        const selectedFilePath = await open({
            multiple: false,
            directory: false,
            title: "Select an image"
        });

        if (selectedFilePath) {
			await invoke('save_image', { message: selectedFilePath });
			await new Promise(resolve => setTimeout(resolve, 1500));
			console.log("Done invoking save_image")

	        window.location.href = '/en/select_image';
        }
    }
</script>


<style>
    :global(body, html) {
        margin: 0;
	    overflow: hidden;
	    height: 100vh;
		width: 100vw;
    }

    .buttonContainer {
	    display: flex;
	    justify-content: center;
	    align-items: center;
	    height: 100%;
	    width: 100%;
	    position: absolute;
	    overflow: hidden;
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
</style>

<main>
	introduction
	<div class="buttonContainer">
        <button id="uploadButton" on:click={handleFileSelection}>Select Image</button>
	</div>
</main>
