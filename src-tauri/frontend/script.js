const { invoke } = window.__TAURI__.tauri;
const { open } = window.__TAURI__.dialog;

document.getElementById('sendFilePathButton').addEventListener('click', async () => {
    try {
        // Open the file dialog to select a file
        const selectedFilePath = await open({
            multiple: false,
            directory: false,
            filters: [{ name: 'Image Files', extensions: ['jpg', 'png', 'gif', 'webp', 'tiff', 'bmp', 'svg'] }]
        });

        if (selectedFilePath) {
            // Log the selected file path
            console.log('Selected file path:', selectedFilePath);

            const displayImage = document.getElementById('displayImage');
            displayImage.src = './processed_image.jpg';
            displayImage.style.display = 'block';
        } else {
            console.error('No file selected');
        }
    } catch (error) {
        console.error('Error processing image:', error);
    }
});
