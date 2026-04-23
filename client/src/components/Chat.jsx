import { useState } from "react";
import axios from "axios";

export default function Chat({
  fileId,
  setTimestamp
}) {
  const [question, setQuestion] =
    useState("");

  const [messages, setMessages] =
    useState([]);

  const [loading, setLoading] =
    useState(false);

  const handleAsk = async () => {
    if (!fileId) {
      alert("Upload file first.");
      return;
    }

    if (!question.trim()) {
      return;
    }

    try {
      setLoading(true);

      // Add user message
      const updatedMessages = [
        ...messages,
        {
          role: "user",
          text: question
        }
      ];

      setMessages(updatedMessages);

      const res = await axios.post(
        "http://127.0.0.1:8000/chat/",
        {
          file_id: fileId,
          question: question
        }
      );

      const {
        answer,
        timestamp
      } = res.data;

      // Add AI message
      setMessages([
        ...updatedMessages,
        {
          role: "ai",
          text: answer,
          timestamp: timestamp
        }
      ]);

      setTimestamp(
        timestamp !== undefined
          ? timestamp
          : null
      );

      setQuestion("");

    } catch (error) {
      console.error(error);

      setMessages([
        ...messages,
        {
          role: "ai",
          text:
            "Something went wrong."
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-4 w-full max-w-2xl mt-6">

      <h2 className="text-lg font-semibold mb-4">
        AI Chat
      </h2>

      {/* Messages */}
      <div className="h-72 overflow-y-auto space-y-3 mb-4 pr-1">

        {messages.map(
          (msg, index) => (
            <div
              key={index}
              className={`max-w-[80%] px-4 py-2 rounded-xl text-sm ${
                msg.role === "user"
                  ? "bg-emerald-500 text-black ml-auto"
                  : "bg-zinc-800 text-white"
              }`}
            >
              <p>{msg.text}</p>

              {/* Timestamp */}
              {msg.timestamp !==
                null &&
                msg.timestamp !==
                  undefined && (
                  <p className="text-xs text-zinc-400 mt-1">
                    ⏱{" "}
                    {Math.floor(
                      msg.timestamp
                    )}{" "}
                    sec
                  </p>
                )}
            </div>
          )
        )}

        {loading && (
          <div className="bg-zinc-800 text-white px-4 py-2 rounded-xl w-fit text-sm">
            Thinking...
          </div>
        )}
      </div>

      {/* Input */}
      <div className="flex gap-2">
        <input
          type="text"
          value={question}
          onChange={(e) =>
            setQuestion(
              e.target.value
            )
          }
          placeholder="Ask something..."
          className="flex-1 bg-zinc-800 text-white px-4 py-2 rounded-lg outline-none"
          onKeyDown={(e) =>
            e.key === "Enter" &&
            handleAsk()
          }
        />

        <button
          onClick={handleAsk}
          disabled={loading}
          className="bg-emerald-500 hover:bg-emerald-600 text-black px-4 py-2 rounded-lg font-medium"
        >
          Send
        </button>
      </div>
    </div>
  );
}