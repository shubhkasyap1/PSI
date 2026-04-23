import { useState } from "react";

import Layout from "./components/Layout";
import Upload from "./components/Upload";
import Chat from "./components/Chat";
import Player from "./components/Player";
import Summary from "./components/Summary";

function App() {
  const [fileId, setFileId] =
    useState(null);

  const [timestamp, setTimestamp] =
    useState(null);

  return (
    <Layout>
      <div className="flex flex-col items-center gap-6">

        {/* Upload */}
        <Upload
          setFileId={setFileId}
        />

        {/* Show after upload */}
        {fileId && (
          <>
            {/* File Info */}
            <div className="w-full max-w-2xl bg-zinc-900 border border-zinc-800 rounded-xl p-4">
              <p className="text-sm text-zinc-300">
                Uploaded File ID:
              </p>

              <p className="text-emerald-400 break-all text-sm mt-1">
                {fileId}
              </p>
            </div>

            {/* Chat */}
            <Chat
              fileId={fileId}
              setTimestamp={
                setTimestamp
              }
            />

            {/* Media Player */}
            <Player
              fileId={fileId}
              timestamp={
                timestamp
              }
            />

            {/* Summary */}
            <Summary
              fileId={fileId}
            />
          </>
        )}

      </div>
    </Layout>
  );
}

export default App;