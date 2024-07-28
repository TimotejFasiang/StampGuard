const { invoke } = window.__TAURI__.tauri;
const { open } = window.__TAURI__.dialog;
const { homeDir } = window.__TAURI__.path;
const { convertFileSrc } = window.__TAURI__.tauri


async function handleFileSelection() {
    const homeDirPath = await homeDir();
    const basePath = `${homeDirPath}.local/share/stamp-guard/frontend`;
    const processedImagePath = `${basePath}/processed_image.jpg`;
    const processedImagePathURL = convertFileSrc(processedImagePath)
    const displayImage = document.getElementById('selectedImage');
    displayImage.src = processedImagePathURL;
}

handleFileSelection()