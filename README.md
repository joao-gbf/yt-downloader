🎬 yt-downloader
Download YouTube videos as MP3 (audio) and/or MP4 (video + audio) at the best available quality.

📋 Requirements
Before you start, make sure you have installed:

Python 3.8+
ffmpeg — must be available in your system PATH

How to check if they are installed
Open your terminal and run:
bashpython --version
ffmpeg -version
If either command is not found, install it before continuing.

⚙️ Installation
1. Clone the repository
bashgit clone https://github.com/your-username/yt-downloader.git
cd yt-downloader
2. Install the dependencies
bashpip install -r requirements.txt

🚀 Usage
1. Run the script
bashpython index.py
2. Paste the YouTube video URL when prompted
Paste the video URL: https://www.youtube.com/watch?v=...
3. Choose what to download
1 - Download audio only (MP3)
2 - Download video + audio (MP4)
3 - Download both (MP3 and MP4)
4. Wait for the download to finish
Files are saved automatically to:
~/Downloads/DownloadsYouTube/
├── VideoTitle_2025-01-15_14-30.mp3
└── VideoTitle_2025-01-15_14-30.mp4

🛠️ Building a standalone .exe (Windows)
If you want to distribute the tool as a single executable with no Python required:
1. Install PyInstaller
bashpip install pyinstaller
2. Build the executable
bashpyinstaller --onefile --add-binary "C:\path\to\ffmpeg.exe;." index.py
3. Run the generated file
dist/index.exe

The .exe will automatically detect the bundled ffmpeg.exe.


⚠️ Disclaimer
This project is intended for personal and educational use only. Please respect the YouTube Terms of Service and the copyright of content creators.

📄 License
MIT
