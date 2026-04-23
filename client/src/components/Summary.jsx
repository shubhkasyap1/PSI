import { useState } from "react";
import axios from "axios";

export default function Summary({
  fileId
}) {
  const [summary, setSummary] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const handleSummary =
    async () => {
      if (!fileId) {
        alert(
          "Upload file first."
        );
        return;
      }

      try {
        setLoading(true);

        const res =
          await axios.post(
            "http://127.0.0.1:8000/summary/",
            {
              file_id: fileId
            }
          );

        setSummary(
          res.data.summary ||
            "No summary available."
        );

      } catch (error) {
        console.error(error);

        setSummary(
          "Failed to generate summary."
        );

      } finally {
        setLoading(false);
      }
    };

  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-4 w-full max-w-2xl mt-6">

      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold">
          Summary
        </h2>

        <button
          onClick={
            handleSummary
          }
          disabled={
            loading
          }
          className="bg-emerald-500 hover:bg-emerald-600 text-black px-4 py-2 rounded-lg font-medium"
        >
          {loading
            ? "Generating..."
            : "Generate Summary"}
        </button>
      </div>

      {/* Content */}
      <div className="bg-zinc-800 rounded-lg p-4 min-h-[140px] text-sm whitespace-pre-line text-zinc-100">

        {loading ? (
          <p>
            Creating summary...
          </p>
        ) : summary ? (
          <p>{summary}</p>
        ) : (
          <p className="text-zinc-400">
            Click the button to generate a summary.
          </p>
        )}

      </div>
    </div>
  );
}