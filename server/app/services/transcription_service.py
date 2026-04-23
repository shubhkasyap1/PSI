import whisper

# Load once
model = whisper.load_model("base")


def transcribe_audio(file_path: str):
    try:
        print("🎧 Transcribing:", file_path)

        result = model.transcribe(
            file_path,
            fp16=False   # important for CPU/Windows
        )

        segments = []

        for seg in result["segments"]:
            text = seg["text"].strip()

            if text:
                segments.append({
                    "text": text,
                    "start": seg["start"],
                    "end": seg["end"]
                })

        print("✅ Segments:", len(segments))

        return segments

    except Exception as e:
        print("❌ Transcription Error:", e)
        return {"error": str(e)}