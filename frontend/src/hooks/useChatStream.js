import { useDispatch } from "react-redux";
import { addMessage, setStreaming, appendStreamChunk, finalizeStream, setSuggestions } from "../store/chatSlice";
import { populateForm } from "../store/formSlice";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export function useChatStream() {
  const dispatch = useDispatch();

  const sendMessage = async (message, interactionId = null) => {
    dispatch(addMessage({ role: "user", content: message }));
    dispatch(setStreaming(true));

    try {
      const response = await fetch(`${API_URL}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, interaction_id: interactionId }),
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const text = decoder.decode(value);
        const lines = text.split("\n").filter((l) => l.startsWith("data: "));

        for (const line of lines) {
          const data = JSON.parse(line.replace("data: ", ""));

          if (data.type === "text") {
            dispatch(appendStreamChunk(data.content));
          } else if (data.type === "form_update") {
            dispatch(populateForm(data.fields));
          } else if (data.type === "suggestions") {
            dispatch(setSuggestions(data.suggestions));
          } else if (data.type === "done") {
            dispatch(finalizeStream());
          }
        }
      }
    } catch (err) {
      dispatch(finalizeStream());
      console.error("Stream error:", err);
    }
  };

  return { sendMessage };
}
