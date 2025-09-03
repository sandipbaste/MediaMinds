import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# List of required packages
packages = [
    "fastapi==0.104.1",
    "uvicorn==0.24.0",
    "streamlit==1.28.0",
    "langchain==0.0.346",
    "google-generativeai==0.3.0",
    "python-dotenv==1.0.0",
    "pydantic==2.5.0",
    "PyPDF2==3.0.1",
    "gtts==2.3.2",
    "moviepy==1.0.3",
    "pillow==10.0.1",
    "python-multipart==0.0.6",
    "pdfplumber==0.10.3"  # Alternative PDF processor
]

print("Installing required packages...")
for package in packages:
    try:
        install(package)
        print(f"✓ Installed {package}")
    except Exception as e:
        print(f"✗ Failed to install {package}: {e}")

print("\nInstallation complete!")