const { invoke } = window.__TAURI__.tauri;
const { open } = window.__TAURI__.dialog;

async function handleFileSelection() {
  const selectedFilePath = await open({multiple: false, directory: false});

  if (selectedFilePath) {
      console.log("Selected file URL:", selectedFilePath);

      await invoke('save_image', { message: selectedFilePath });

      // TODO: Call ↓↓↓ when confirmButton clicked, will increase performance.(code currently in save_image.py)
      // await invoke('process_image', { message: selectedFilePath });

      const displayImage = document.getElementById('selectedImage');
      displayImage.src = './orig_image.jpg';
      displayImage.style.display = 'block';

      document.getElementById('uploadButton').style.display = 'none';
      document.getElementById('buttonRow').style.display = 'flex';
  }
}

document.getElementById('confirmButton').addEventListener('click', async function() {
    window.location.href = 'display-image-en.html';
});

document.getElementById('uploadButton').addEventListener('click', handleFileSelection);
document.getElementById('chooseAnotherButton').addEventListener('click', handleFileSelection);
