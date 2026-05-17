from pytubefix import YouTube
import subprocess
import os
import sys
import re
import unicodedata
from datetime import datetime

# ── Locate ffmpeg.exe (bundled in .exe or system PATH) ───────────────────────
def get_ffmpeg():
    # When running as a .exe built by PyInstaller, extra files
    # are in the temporary folder pointed to by sys._MEIPASS
    if getattr(sys, "frozen", False):
        path = os.path.join(sys._MEIPASS, "ffmpeg.exe")
        if os.path.exists(path):
            return path
    # Fallback: use ffmpeg installed in the system PATH
    return "ffmpeg"

FFMPEG = get_ffmpeg()

# ── Output folder ─────────────────────────────────────────────────────────────
OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "DownloadsYouTube")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Sanitize filenames (Windows-safe) ────────────────────────────────────────
def sanitize_filename(name, max_length=100):
    name = unicodedata.normalize("NFKD", name)
    name = name.encode("ASCII", "ignore").decode("ASCII")
    name = name.replace(" ", "_")
    name = re.sub(r'[\\/:*?"<>|&%$#@!+=\[\]{};,\'`^~]', "", name)
    name = re.sub(r'[\x00-\x1f\x7f]', "", name)
    name = re.sub(r'_+', "_", name).strip("_")
    if len(name) > max_length:
        name = name[:max_length].rstrip("_")
    return name or "video"

# ── Run ffmpeg and show log on error ─────────────────────────────────────────
def run_ffmpeg(args, description=""):
    print(f"\n  → ffmpeg: {description}")
    result = subprocess.run(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace"
    )
    if result.returncode != 0:
        print("\n  ffmpeg ERROR:")
        print(result.stderr[-2000:])
        return False
    return True

# ── Convert audio to AAC (fixes Opus not supported in MP4) ───────────────────
def convert_audio_to_aac(audio_in, aac_out):
    return run_ffmpeg(
        [FFMPEG, "-y", "-i", audio_in, "-vn", "-c:a", "aac", "-b:a", "192k", aac_out],
        "converting audio Opus → AAC"
    )

# ── Generate MP3 ──────────────────────────────────────────────────────────────
def generate_mp3(audio_in, output):
    return run_ffmpeg(
        [FFMPEG, "-y", "-i", audio_in, "-vn", "-ab", "192k", "-ar", "44100", "-f", "mp3", output],
        f"generating MP3 → {os.path.basename(output)}"
    )

# ── Generate MP4 (video + AAC audio) ─────────────────────────────────────────
def generate_mp4(video_in, aac_in, output):
    return run_ffmpeg(
        [FFMPEG, "-y", "-i", video_in, "-i", aac_in,
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-movflags", "+faststart", output],
        f"generating MP4 → {os.path.basename(output)}"
    )

# ── Delete temporary files ────────────────────────────────────────────────────
def cleanup(*files):
    for f in files:
        if f and os.path.exists(f):
            try:
                os.remove(f)
            except Exception:
                pass

# ═════════════════════════════════════════════════════════════════════════════
# MAIN
# ═════════════════════════════════════════════════════════════════════════════
print("=" * 55)
print("  YouTube Downloader  —  MP3 / MP4 / Both")
print("=" * 55)

url = input("\nPaste the video URL: ").strip()
if not url:
    input("\nEmpty URL. Press Enter to exit.")
    sys.exit(1)

print("\nLoading video information...")
try:
    yt = YouTube(url)
    raw_title = yt.title
    author    = yt.author
except Exception as e:
    print(f"\nError accessing video: {e}")
    input("Press Enter to exit.")
    sys.exit(1)

print(f"  Title  : {raw_title}")
print(f"  Author : {author}")

title     = sanitize_filename(raw_title)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
base_name = f"{title}_{timestamp}"

print("\nChoose an option:")
print("  1 - Download audio only (MP3)")
print("  2 - Download video + audio (MP4)")
print("  3 - Download both (MP3 and MP4)")
option = input("Enter 1, 2 or 3: ").strip()

if option not in ("1", "2", "3"):
    input("\nInvalid option. Press Enter to exit.")
    sys.exit(1)

# Streams
video_stream = (yt.streams
                  .filter(adaptive=True, type="video")
                  .order_by("resolution").desc().first())
audio_stream = (yt.streams
                  .filter(adaptive=True, only_audio=True)
                  .order_by("abr").desc().first())

AUDIO_TEMP = "yt_audio_temp.webm"
VIDEO_TEMP = "yt_video_temp.mp4"
AAC_TEMP   = "yt_audio_aac.m4a"

# ── Option 1: MP3 only ────────────────────────────────────────────────────────
if option == "1":
    print("\nDownloading audio...")
    audio_stream.download(filename=AUDIO_TEMP)

    output = os.path.join(OUTPUT_DIR, f"{base_name}.mp3")
    ok = generate_mp3(AUDIO_TEMP, output)
    cleanup(AUDIO_TEMP)
    print(f"\n{'OK  MP3 generated' if ok else 'ERROR generating MP3'}: {output}")

# ── Option 2: MP4 only ────────────────────────────────────────────────────────
elif option == "2":
    print(f"\nDownloading video ({video_stream.resolution}) and audio...")
    video_stream.download(filename=VIDEO_TEMP)
    audio_stream.download(filename=AUDIO_TEMP)

    if not convert_audio_to_aac(AUDIO_TEMP, AAC_TEMP):
        cleanup(AUDIO_TEMP, VIDEO_TEMP, AAC_TEMP)
        input("\nAudio conversion error. Press Enter to exit.")
        sys.exit(1)

    output = os.path.join(OUTPUT_DIR, f"{base_name}.mp4")
    ok = generate_mp4(VIDEO_TEMP, AAC_TEMP, output)
    cleanup(AUDIO_TEMP, VIDEO_TEMP, AAC_TEMP)
    print(f"\n{'OK  MP4 generated' if ok else 'ERROR generating MP4'}: {output}")

# ── Option 3: MP3 + MP4 ───────────────────────────────────────────────────────
elif option == "3":
    print(f"\nDownloading video ({video_stream.resolution}) and audio...")
    video_stream.download(filename=VIDEO_TEMP)
    audio_stream.download(filename=AUDIO_TEMP)

    if not convert_audio_to_aac(AUDIO_TEMP, AAC_TEMP):
        cleanup(AUDIO_TEMP, VIDEO_TEMP, AAC_TEMP)
        input("\nAudio conversion error. Press Enter to exit.")
        sys.exit(1)

    output_mp4 = os.path.join(OUTPUT_DIR, f"{base_name}.mp4")
    ok_mp4 = generate_mp4(VIDEO_TEMP, AAC_TEMP, output_mp4)
    print(f"\n{'OK  MP4 generated' if ok_mp4 else 'ERROR generating MP4'}: {output_mp4}")

    output_mp3 = os.path.join(OUTPUT_DIR, f"{base_name}.mp3")
    ok_mp3 = generate_mp3(AAC_TEMP, output_mp3)
    print(f"{'OK  MP3 generated' if ok_mp3 else 'ERROR generating MP3'}: {output_mp3}")

    cleanup(AUDIO_TEMP, VIDEO_TEMP, AAC_TEMP)

input("\nDone! Press Enter to close.")