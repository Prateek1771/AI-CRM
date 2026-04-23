import { useDispatch, useSelector } from "react-redux";
import { resetForm, setSaving, setSavedId } from "../../store/formSlice";
import client from "../../api/client";

export default function FormActions() {
  const dispatch = useDispatch();
  const form = useSelector((s) => s.form);

  const handleSave = async () => {
    dispatch(setSaving(true));
    try {
      const payload = {
        hcp_id: form.hcp_id,
        interaction_type: form.interaction_type,
        date: form.date,
        time: form.time || null,
        attendees: form.attendees,
        topics_discussed: form.topics_discussed,
        materials_shared: form.materials_shared,
        samples_distributed: form.samples_distributed,
        sentiment: form.sentiment,
        outcomes: form.outcomes,
        follow_up_actions: form.follow_up_actions,
        follow_up_date: form.follow_up_date || null,
      };
      const res = form.savedInteractionId
        ? await client.patch(`/api/interactions/${form.savedInteractionId}`, payload)
        : await client.post("/api/interactions", payload);
      dispatch(setSavedId(res.data.id));
      alert("Interaction saved!");
    } catch (err) {
      console.error(err);
      alert("Failed to save. Please try again.");
    } finally {
      dispatch(setSaving(false));
    }
  };

  return (
    <div className="flex justify-end gap-3 pt-4 border-t border-gray-100">
      <button
        onClick={() => dispatch(resetForm())}
        className="px-4 py-2 text-sm text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50"
      >
        Cancel
      </button>
      <button
        onClick={handleSave}
        disabled={form.isSaving}
        className="px-6 py-2 text-sm text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:opacity-50"
      >
        {form.isSaving ? "Saving..." : "Save Log"}
      </button>
    </div>
  );
}
