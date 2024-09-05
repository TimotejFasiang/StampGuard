use tauri::command;
use tauri::api::process::{Command, CommandEvent};
use std::fs::OpenOptions;
use std::io::Write;

#[command]
async fn save_image(window: tauri::Window, message: String) {
    // Pass the `message` (which is the file path) as an argument to the Python script
    let (mut rx, mut child) = Command::new_sidecar("save_image")
        .expect("failed to create `save_image` binary command")
        .args([&message])
        .spawn()
        .expect("Failed to spawn sidecar");

    tauri::async_runtime::spawn(async move {
        while let Some(event) = rx.recv().await {
            match event {
                CommandEvent::Stdout(line) | CommandEvent::Stderr(line) => {
                    log_to_file(&line); // Log each line of output
                    window
                        .emit("message", Some(format!("'{}'", line)))
                        .expect("failed to emit event");
                }
                _ => {}
            }
        }
    });
}

fn log_to_file(message: &str) {
    let log_file_path = "/home/timotej/Desktop/app_log.txt";

    let mut file = OpenOptions::new()
        .create(true)
        .append(true)
        .open(log_file_path)
        .expect("Failed to open log file");

    writeln!(file, "{}", message).expect("Failed to write to log file");
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![save_image])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
