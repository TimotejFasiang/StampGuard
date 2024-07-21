const { invoke } = window.__TAURI__.tauri

document.getElementById('uploadButton').addEventListener('click', function() {
    document.getElementById('fileInput').click();
});

document.getElementById('fileInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const img = document.getElementById('selectedImage');
            img.src = e.target.result;
            img.style.display = 'block';
            document.getElementById('uploadButton').style.display = 'none';
            document.getElementById('buttonRow').style.display = 'flex';
        }
        reader.readAsDataURL(file);
    }
});

document.getElementById('confirmButton').addEventListener('click', async function() {
    const fileInput = document.getElementById('fileInput');
    if (fileInput.files.length > 0) {
        const file = fileInput.files[0];
        const filePath = URL.createObjectURL(file); // Create a URL for the file

        try {
            // Call the Tauri command with the file path
            await invoke('process_image', { message: filePath });

            // Redirect after the command completes
            window.location.href = 'display-image-en.html';
        } catch (error) {
            console.error('Error invoking Tauri command:', error);
        }
    } else {
        console.warn('No file selected.');
    }
});

document.getElementById('chooseAnotherButton').addEventListener('click', function() {
    document.getElementById('fileInput').click();
});
