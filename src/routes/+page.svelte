<script lang="ts">
    import { onMount } from 'svelte';
    import { writeTextFile, readTextFile, createDir, exists } from '@tauri-apps/api/fs';
    import { homeDir } from '@tauri-apps/api/path';

    // Helper function to get the settings file path
    async function getSettingsPath() {
        try {
            console.log("Getting the home directory path...");
            const homeDirPath = await homeDir();
            const basePath = `${homeDirPath}.local/share/stamp-guard/frontend`;
            const settingsPath = `${basePath}/settings.json`;

            console.log("Checking if settings directory exists...");
            const dirExists = await exists(basePath);
            if (!dirExists) {
                console.log("Directory does not exist, creating directory...");
                await createDir(basePath, { recursive: true });
            } else {
                console.log("Directory already exists.");
            }

            console.log(`Settings file path: ${settingsPath}`);
            return settingsPath;
        } catch (error) {
            console.error("Error getting settings path:", error);
            throw error;
        }
    }

    // Function to save settings to the file
    async function saveSettings(settings) {
        try {
            console.log("Saving settings:", settings);
            const settingsPath = await getSettingsPath();
            const settingsJSON = JSON.stringify(settings);
            await writeTextFile(settingsPath, settingsJSON);
            console.log("Settings saved successfully.");
        } catch (error) {
            console.error("Error saving settings:", error);
        }
    }

    // Function to update a specific setting and save it
    async function updateSetting(key, value) {
        try {
            console.log(`Updating setting: ${key} = ${value}`);
            const currentSettings = await getSettings();
            currentSettings[key] = value;
            await saveSettings(currentSettings);
        } catch (error) {
            console.error("Error updating setting:", error);
        }
    }

    // Function to retrieve settings from the file
    async function getSettings() {
        try {
            console.log("Retrieving settings...");
            const settingsPath = await getSettingsPath();
            const settingsJSON = await readTextFile(settingsPath);
            const settings = JSON.parse(settingsJSON);
            console.log("Settings retrieved:", settings);
            return settings;
        } catch (error) {
            console.warn("Settings file not found or corrupted. Returning default settings.");
            return {}; // Return default settings if the file doesn't exist or is corrupted
        }
    }

    // Function to get the saved language preference
    async function getLanguagePreference() {
        try {
            console.log("Getting language preference...");
            const settings = await getSettings();
            const language = settings.language || null;
            console.log(`Language preference found: ${language}`);
            return language;
        } catch (error) {
            console.error("Error getting language preference:", error);
            return null;
        }
    }

    // Function to handle button clicks and save language preference
    async function handleClick(language: string) {
        console.log(`Button clicked for language: ${language}`);
        try {
            await updateSetting('language', language);  // Ensure the setting is saved before redirecting
            console.log("Language preference saved successfully.");

            if (language === "english") {
                console.log("Redirecting to English introduction page...");
                window.location.href = "/en/introduction";
            } else if (language === "czech") {
                console.log("Redirecting to Czech introduction page...");
                window.location.href = "/cz/introduction";
            }
        } catch (error) {
            console.error("Error saving language preference:", error);
        }
    }

    // When the component mounts, check for the saved language preference
    onMount(async () => {
        try {
            console.log("Component mounted. Checking for saved language preference...");
            const language = await getLanguagePreference();
            if (language) {
                console.log(`Language preference exists: ${language}. Redirecting...`);
                handleClick(language);
            } else {
                console.log("No language preference found. Awaiting user selection...");
                const buttons = document.querySelectorAll("button");
                buttons.forEach(button => {
                    button.addEventListener("click", () => {
                        const language = button.getAttribute("data-language") as string;
                        handleClick(language);
                    });
                });
            }
        } catch (error) {
            console.error("Error during component initialization:", error);
        }
    });
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

    .image-button-wrapper img {
	    max-height: calc(90vh - 55px);
        max-width: 90vw;
        width: auto;
        height: auto;
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

    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }

    @keyframes resizeAndMove {
        0% {
            transform: scale(1) translateY(0);
        }
        100% {
            transform: scale(0.75) translateY(-10%);
        }
    }

    @keyframes fadeInButtons {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
</style>

<main>
    <div class="container">
        <div class="image-button-wrapper">
	        <img src="/png/logo-light.png" alt="Logo">

	        <div class="button-row">
	            <button data-language="english">Continue (English)</button>
	            <button data-language="czech">Pokračovat (Čeština)</button>
	        </div>
        </div>
    </div>
</main>