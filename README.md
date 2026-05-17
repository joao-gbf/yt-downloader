🎬 YouTube Downloader — MP3 / MP4
A command-line tool to download YouTube videos as MP3 (audio only) and/or MP4 (video + audio) at the best available quality.

✨ Features

🎵 Audio download as MP3 (192 kbps, 44100 Hz)
🎬 Video download as MP4 at the highest available resolution
🔀 Download both formats at once (MP3 + MP4)
🔁 Automatic audio conversion from Opus/WebM → AAC (MP4-compatible)
🧹 Automatic cleanup of temporary files
📁 Files saved to ~/Downloads/DownloadsYouTube/ with timestamp in the filename
🪟 Windows-compatible, including distribution as a standalone .exe via PyInstaller


🚀 Getting started
Prerequisites

Python 3.8+
ffmpeg installed and available in your system PATH

Installation
bashpip install pytubefix
Usage
bashpython downloader.py
Paste the video URL when prompted and choose an option:
1 - Download audio only (MP3)
2 - Download video + audio (MP4)
3 - Download both (MP3 and MP4)

📦 Dependencies
PackagePurposepytubefixFetch YouTube streamsffmpegAudio/video conversion and muxing

ffmpeg must be installed on your system and available in PATH, or placed in the same folder as the .exe.


🛠️ Building a standalone executable
The script is compatible with PyInstaller. To bundle it:
bashpip install pyinstaller
pyinstaller --onefile --add-binary "ffmpeg.exe;." downloader.py
The generated .exe automatically detects the bundled ffmpeg.exe.

📂 Output structure
Files are saved to:
~/Downloads/DownloadsYouTube/
├── VideoTitle_2025-01-15_14-30.mp3
└── VideoTitle_2025-01-15_14-30.mp4

⚠️ Disclaimer
This project is intended for personal and educational use only. Please respect the YouTube Terms of Service and the copyright of content creators.

📄 License
MIT
