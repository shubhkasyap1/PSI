import { useEffect, useRef, useState } from "react";

export default function Player({ fileId, timestamp }) {
  const mediaRef = useRef(null);
  const [fileType, setFileType] = useState("video");
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    if (!fileId) return;

    const lower = fileId.toLowerCase();

    // Detect media type
    if (
      lower.endsWith(".mp3") ||
      lower.endsWith(".wav") ||
      lower.endsWith(".m4a") ||
      lower.endsWith(".aac")
    ) {
      setFileType("audio");
    } else {
      setFileType("video");
    }

    setIsReady(false);
  }, [fileId]);

  if (!fileId) return null;

  const mediaUrl = `http://127.0.0.1:8000/uploads/${fileId}`;

  const handleJump = async () => {
    const media = mediaRef.current;

    if (!media) return;

    const jumpTime = Number(timestamp) || 0;

    // If metadata not loaded yet, wait
    if (!isReady) {
      media.load();
      return;
    }

    try {
      media.currentTime = jumpTime;
      await media.play();
    } catch (error) {
      console.error("Playback error:", error);
    }
  };

  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-4 w-full max-w-2xl mt-6">

      <h2 className="text-lg font-semibold mb-4">
        Media Player
      </h2>

      {/* Video */}
      {fileType === "video" ? (
        <video
          ref={mediaRef}
          controls
          className="w-full rounded-lg mb-4"
          preload="metadata"
          onLoadedMetadata={() => setIsReady(true)}
        >
          <source src={mediaUrl} />
          Your browser does not support video.
        </video>
      ) : (
        <audio
          ref={mediaRef}
          controls
          className="w-full mb-4"
          preload="metadata"
          onLoadedMetadata={() => setIsReady(true)}
        >
          <source src={mediaUrl} />
          Your browser does not support audio.
        </audio>
      )}

      {/* Timestamp Button */}
      {timestamp !== null &&
        timestamp !== undefined && (
          <button
            onClick={handleJump}
            className="bg-emerald-500 hover:bg-emerald-600 px-4 py-2 rounded-lg text-black font-medium"
          >
            ▶ Play Relevant Part (
            {Math.floor(Number(timestamp))} sec)
          </button>
        )}
    </div>
  );
}