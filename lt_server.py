import os
import subprocess
import socket
import time

# Path to your LanguageTool folder
LT_PATH = r"C:\Users\JAGADISH\.languagetool\LanguageTool-6.6"
PORT = 8081

def is_port_in_use(port):
    """Check if a port is already in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0

def start_languagetool_server():
    """Start the LanguageTool server if not already running."""
    if is_port_in_use(PORT):
        print(f"✅ LanguageTool server is already running on port {PORT}.")
        return

    print("🚀 Starting LanguageTool server...")
    jar_path = os.path.join(LT_PATH, "languagetool-server.jar")

    # Launch Java LanguageTool server in the background
    process = subprocess.Popen(
        ["java", "-cp", jar_path, "org.languagetool.server.HTTPServer", "--port", str(PORT)],
        cwd=LT_PATH,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        shell=True
    )

    # Wait a few seconds to ensure it starts
    time.sleep(5)

    if is_port_in_use(PORT):
        print(f"✅ LanguageTool server started successfully on port {PORT}.")
    else:
        print("❌ Failed to start LanguageTool server. Check Java installation or path.")
    return process

if __name__ == "__main__":
    start_languagetool_server()
