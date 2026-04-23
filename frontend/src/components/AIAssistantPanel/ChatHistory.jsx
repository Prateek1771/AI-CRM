import { useSelector } from "react-redux";
import { useEffect, useRef } from "react";

export default function ChatHistory() {
  const { messages, isStreaming, streamingContent } = useSelector((s) => s.chat);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, streamingContent]);

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-3">
      {messages.map((msg, i) => (
        <div
          key={i}
          className={`rounded-lg px-4 py-3 text-sm ${
            msg.role === "user"
              ? "bg-blue-50 border-l-4 border-blue-400 ml-4"
              : msg.role === "assistant" && i === 0
              ? "bg-sky-50 text-gray-700"
              : "bg-green-50 border border-green-200 text-gray-800"
          }`}
        >
          {msg.content}
        </div>
      ))}
      {isStreaming && streamingContent && (
        <div className="bg-green-50 border border-green-200 rounded-lg px-4 py-3 text-sm text-gray-800">
          {streamingContent}
          <span className="animate-pulse">▋</span>
        </div>
      )}
      <div ref={bottomRef} />
    </div>
  );
}
