<script lang="ts">
    import { open } from '@tauri-apps/plugin-dialog';
	import { Command } from "@tauri-apps/plugin-shell";

    // Function to handle file selection and invoke the command
    async function handleFileSelection() {
        console.log("Starting handleFileSelection")
        const selectedFilePath = await open({
            multiple: false,
            directory: false,
            title: "Select an image"
        });

        if (selectedFilePath) {
        	console.log("Invoking save_image");

			try {
				const command = Command.sidecar('src/save_image', [selectedFilePath]);
				const output = await command.execute();  // Executes and waits for result

				console.log(`[Python stdout]: ${output.stdout}`);
				console.error(`[Python stderr]: ${output.stderr}`);

				if (output.code !== 0) {
					console.error(`Process exited with error code: ${output.code}`);
				}
			} catch (error) {
				console.error(`Command execution error: ${error}`);
			}

			console.log("Done invoking save_image");

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
	<div class="buttonContainer">
        <button id="uploadButton" on:click={handleFileSelection}>Vybrat obrázek</button>
	</div>
</main>
