import { useState } from "react";
import { useSelector } from "react-redux";
import { useChatStream } from "../../hooks/useChatStream";

export default function ChatInput() {
  const [value, setValue] = useState("");
  const { isStreaming } = useSelector((s) => s.chat);
  const { savedInteractionId } = useSelector((s) => s.form);
  const { sendMessage } = useChatStream();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!value.trim() || isStreaming) return;
    sendMessage(value.trim(), savedInteractionId);
    setValue("");
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 border-t border-gray-100">
      <div className="flex gap-2">
        <input
          type="text"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder="Describe Interaction..."
          disabled={isStreaming}
          className="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400 disabled:bg-gray-50"
        />
        <button
          type="submit"
          disabled={isStreaming || !value.trim()}
          className="w-10 h-10 bg-blue-600 text-white rounded-full flex items-center justify-center disabled:opacity-50 hover:bg-blue-700"
        >
          ▶
        </button>
      </div>
    </form>
  );
}
