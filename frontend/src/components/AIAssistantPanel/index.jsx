import ChatHistory from "./ChatHistory";
import ChatInput from "./ChatInput";
import SuggestionChips from "./SuggestionChips";

export default function AIAssistantPanel() {
  return (
    <div className="flex flex-col h-full bg-white border-l border-gray-200">
      <div className="px-4 py-3 border-b border-gray-100">
        <div className="flex items-center gap-2">
          <span className="text-lg">🤖</span>
          <div>
            <div className="font-semibold text-gray-800 text-sm">AI Assistant</div>
            <div className="text-xs text-gray-500">Log Interaction details here via chat</div>
          </div>
        </div>
      </div>
      <ChatHistory />
      <SuggestionChips />
      <ChatInput />
    </div>
  );
}
