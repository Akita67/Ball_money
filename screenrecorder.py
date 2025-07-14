import subprocess

class ScreenRecorder:
    """
    A class to handle screen recording using FFmpeg in a separate process.
    This is optimized for real-time capture by using hardware encoding (NVENC)
    with a fallback to efficient CPU encoding (libx264).
    """
    def __init__(self, width, height, fps, window_title, output_file="recording.mp4", encoder="nvenc"):
        self.width = width
        self.height = height
        self.fps = fps
        self.window_title = window_title
        self.output_file = output_file
        self.encoder = encoder.lower()
        self.recorder_process = None

        # --- IMPORTANT ---
        # You MUST find the correct audio device name on your system.
        # Run this command in your terminal to list devices:
        # ffmpeg -list_devices true -f dshow -i dummy
        self.audio_device = "Stereo Mix (Realtek(R) Audio)" # <-- CHANGE THIS IF NEEDED

    def _get_nvenc_cmd(self):
        """Returns the FFmpeg command for NVIDIA hardware encoding."""
        print("Using NVIDIA NVENC hardware encoder.")
        return [
            "ffmpeg", "-y", "-hide_banner",
            # "-loglevel", "error", # Temporarily commented out to see all output for debugging

            # Video Input: gdigrab for window capture
            "-f", "gdigrab",
            "-framerate", str(self.fps),
            "-thread_queue_size", "1024",
            "-i", f"title={self.window_title}",

            # Audio Input: dshow for system audio
            "-f", "dshow",
            "-thread_queue_size", "1024",
            "-i", f"audio={self.audio_device}",

            # Video Codec: H.264 NVENC
            "-c:v", "h264_nvenc",
            "-preset", "p4",
            "-rc", "vbr",
            "-b:v", "8M",
            "-maxrate", "10M",
            "-bufsize", "10M",
            "-pix_fmt", "yuv420p",
            "-vsync", "cfr",

            # Audio Codec
            "-c:a", "aac",
            "-b:a", "192k",

            self.output_file
        ]

    def _get_cpu_cmd(self):
        """Returns the FFmpeg command for CPU (libx264) encoding."""
        print("Using CPU-based libx264 encoder. This will use more CPU.")
        return [
            "ffmpeg", "-y", "-hide_banner",
            # "-loglevel", "error", # Temporarily commented out to see all output for debugging

            # Video and Audio Inputs (same as NVENC)
            "-f", "gdigrab",
            "-framerate", str(self.fps),
            "-thread_queue_size", "1024",
            "-i", f"title={self.window_title}",
            "-f", "dshow",
            "-thread_queue_size", "1024",
            "-i", f"audio={self.audio_device}",

            # Video Codec: libx264
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-crf", "23",
            "-pix_fmt", "yuv420p",
            "-vsync", "cfr",

            # Audio Codec
            "-c:a", "aac",
            "-b:a", "192k",

            self.output_file
        ]

    def start(self):
        """Starts the FFmpeg recording process."""
        if self.recorder_process is not None:
            print("Recorder is already running.")
            return

        if self.encoder == "nvenc":
            cmd = self._get_nvenc_cmd()
        else:
            cmd = self._get_cpu_cmd()

        try:
            # Removed DEVNULL to allow FFmpeg's output to appear in the console for debugging.
            self.recorder_process = subprocess.Popen(cmd, stdin=subprocess.PIPE)
            print(f"Recorder started. Outputting to {self.output_file}")
        except FileNotFoundError:
            print("ERROR: ffmpeg not found. Make sure it's in your system's PATH.")
            self.recorder_process = None
        except Exception as e:
            print(f"ERROR: Failed to start recorder. Check your FFmpeg command and audio device name.")
            print(f"  Details: {e}")
            if self.encoder == "nvenc":
                print("...Attempting to fall back to CPU encoder.")
                self.encoder = "cpu"
                self.start()


    def stop(self):
        """Stops the FFmpeg recording process gracefully."""
        if self.recorder_process is None:
            return

        print("Stopping recorder...")
        try:
            self.recorder_process.stdin.write(b'q\n')
            self.recorder_process.stdin.flush()
            self.recorder_process.wait(timeout=5)
            print("Recorder stopped successfully.")
        except (OSError, BrokenPipeError):
            print("Warning: FFmpeg process already terminated.")
        except subprocess.TimeoutExpired:
            print("Warning: FFmpeg did not stop gracefully. Forcing termination.")
            self.recorder_process.kill()
        finally:
            self.recorder_process = None