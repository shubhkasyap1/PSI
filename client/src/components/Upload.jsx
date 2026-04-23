import { useState } from "react";
import axios from "axios";

export default function Upload({ setFileId }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file");
      return;
    }

    try {
      setLoading(true);

      const formData = new FormData();
      formData.append("file", file);

      const res = await axios.post(
        "http://127.0.0.1:8000/upload/",
        formData
      );

      setFileId(res.data.stored_filename)

      alert("✅ File uploaded successfully!");
    } catch (err) {
      console.error(err);
      alert("❌ Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-zinc-900 p-6 rounded-xl border border-zinc-800 w-full max-w-xl">

      <h2 className="text-lg font-semibold mb-4">Upload File</h2>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
        className="mb-4 w-full text-sm text-zinc-400"
      />

      <button
        onClick={handleUpload}
        disabled={loading}
        className="bg-emerald-500 hover:bg-emerald-600 px-4 py-2 rounded-lg w-full"
      >
        {loading ? "Uploading..." : "Upload"}
      </button>
    </div>
  );
}