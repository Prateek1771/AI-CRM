import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  messages: [
    {
      role: "assistant",
      content: 'Log interaction details here (e.g., "Met Dr. Smith, discussed Product X efficacy, positive sentiment, shared brochure") or ask for help.',
    },
  ],
  isStreaming: false,
  streamingContent: "",
  suggestions: [],
  sessionId: null,
};

const chatSlice = createSlice({
  name: "chat",
  initialState,
  reducers: {
    addMessage: (state, action) => {
      state.messages.push(action.payload);
    },
    setStreaming: (state, action) => {
      state.isStreaming = action.payload;
    },
    appendStreamChunk: (state, action) => {
      state.streamingContent += action.payload;
    },
    finalizeStream: (state) => {
      if (state.streamingContent) {
        state.messages.push({ role: "assistant", content: state.streamingContent });
        state.streamingContent = "";
      }
      state.isStreaming = false;
    },
    setSuggestions: (state, action) => {
      state.suggestions = action.payload;
    },
  },
});

export const { addMessage, setStreaming, appendStreamChunk, finalizeStream, setSuggestions } = chatSlice.actions;
export default chatSlice.reducer;
