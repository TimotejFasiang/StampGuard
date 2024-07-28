const { invoke } = window.__TAURI__.tauri;
const { open } = window.__TAURI__.dialog;
const { homeDir } = window.__TAURI__.path;
const { convertFileSrc } = window.__TAURI__.tauri;

async function handleFileSelection() {
    let selectedFilePath = await open({ multiple: false, directory: false, title: "Select an image" });
    if (selectedFilePath) {
        let homeDirPath = await homeDir();
        let basePath = `${homeDirPath}.local/share/stamp-guard/frontend`;
        let origImagePath = `${basePath}/orig_image.jpg`;

        // Invoke the save_image command
        await invoke('save_image', { message: selectedFilePath });

        // Cache busting: Add a unique query parameter to the image URL
        let origImagePathURL = `${convertFileSrc(origImagePath)}?t=${new Date().getTime()}`;

        // Update the image element
        let displayImage = document.getElementById('selectedImage');

        displayImage.src = origImagePathURL; // Set the new src with cache busting
        displayImage.style.display = 'block'; // Show the image

        document.getElementById('uploadButton').style.display = 'none';
        document.getElementById('buttonRow').style.display = 'flex';
    }
}

document.getElementById('confirmButton').addEventListener('click', async function() {
    window.location.href = 'display-image-en.html';
});

document.getElementById('uploadButton').addEventListener('click', handleFileSelection);
document.getElementById('chooseAnotherButton').addEventListener('click', handleFileSelection);
