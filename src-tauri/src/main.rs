use std::fs::OpenOptions;
use std::io::prelude::*;
use std::process::Command;
use tauri::command;

// Function to log messages to a file
fn log_to_file(message: &str) {
    // Define the log file path
    let log_file_path = "./app_log.txt"; // Change this path if needed

    // Open the file in append mode
    let mut file = OpenOptions::new()
        .create(true)
        .append(true)
        .open(log_file_path)
        .expect("Failed to open log file");

    // Write the message to the file
    writeln!(file, "{}", message).expect("Failed to write to log file");
}

// //PY file
// #[command]
// fn save_image(message: String) {
//     let python_script_path = "./src/save_image.py";
//     let current_dir = std::env::current_dir().unwrap();
//     println!("Current directory: {:?}", current_dir);
//     println!("Executable path: {}", python_script_path);
//
//     let output = Command::new("python3")
//         .arg(python_script_path)
//         .arg(&message)  // Pass the selected file path as an argument to Python script
//         .output()
//         .expect("Failed to execute Python script");
//
//     let output_str = String::from_utf8_lossy(&output.stdout);
//     println!("{}", output_str); // Print any python output
// }

//PY executable
#[command]
fn save_image(message: String) {
    let python_script_path = "./src/save_image"; // Path to the executable
    let current_dir = std::env::current_dir().unwrap();
    let log_message = format!("Current directory: {:?}", current_dir);
    log_to_file(&log_message);
    let log_message = format!("Executable path: {}", python_script_path);
    log_to_file(&log_message);

    let output = Command::new(python_script_path) // Call the executable directly
        .arg(&message)  // Pass the selected file path as an argument to the script
        .output();

    match output {
        Ok(output) => {
            if !output.status.success() {
                let error_str = String::from_utf8_lossy(&output.stderr);
                let log_message = format!("Error: {}", error_str);
                log_to_file(&log_message);
            }

            let output_str = String::from_utf8_lossy(&output.stdout);
            let log_message = format!("{}", output_str); // Log any Python output
            log_to_file(&log_message);
        },
        Err(e) => {
            let log_message = format!("Failed to execute Python script: {:?}", e);
            log_to_file(&log_message);
        }
    }
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![save_image])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
