import { useSelector } from "react-redux";
import { useChatStream } from "../../hooks/useChatStream";

export default function SuggestionChips() {
  const { suggestions } = useSelector((s) => s.chat);
  const { sendMessage } = useChatStream();

  if (!suggestions.length) return null;

  return (
    <div className="px-4 pb-2 flex flex-wrap gap-2">
      {suggestions.map((s, i) => (
        <button
          key={i}
          onClick={() => sendMessage(s)}
          className="text-xs bg-blue-100 text-blue-700 rounded-full px-3 py-1 hover:bg-blue-200"
        >
          {s}
        </button>
      ))}
    </div>
  );
}
