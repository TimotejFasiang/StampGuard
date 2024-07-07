use std::process::Command;
use tauri::command;

#[command]
fn print_message(message: String) {
    let python_script_path = "./src/process_image.py";

    let output = Command::new("python3")
        .arg(python_script_path)
        .arg(&message)  // Pass the selected file path as an argument to Python script
        .output()
        .expect("Failed to execute Python script");

    let output_str = String::from_utf8_lossy(&output.stdout);
    println!("{}", output_str); // Print any python output
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![print_message])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
