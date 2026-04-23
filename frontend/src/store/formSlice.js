import { createSlice } from "@reduxjs/toolkit";

const today = new Date().toISOString().split("T")[0];

const initialState = {
  hcp_name: "",
  hcp_id: null,
  interaction_type: "Meeting",
  date: today,
  time: "",
  attendees: [],
  topics_discussed: "",
  materials_shared: [],
  samples_distributed: [],
  sentiment: null,
  outcomes: "",
  follow_up_actions: "",
  follow_up_date: null,
  isSaving: false,
  savedInteractionId: null,
};

const formSlice = createSlice({
  name: "form",
  initialState,
  reducers: {
    setField: (state, action) => {
      const { field, value } = action.payload;
      state[field] = value;
    },
    populateForm: (state, action) => {
      const fields = action.payload;
      Object.keys(fields).forEach((key) => {
        if (key in state && fields[key] !== null && fields[key] !== undefined) {
          state[key] = fields[key];
        }
      });
    },
    setSaving: (state, action) => {
      state.isSaving = action.payload;
    },
    setSavedId: (state, action) => {
      state.savedInteractionId = action.payload;
    },
    resetForm: () => initialState,
  },
});

export const { setField, populateForm, setSaving, setSavedId, resetForm } = formSlice.actions;
export default formSlice.reducer;
