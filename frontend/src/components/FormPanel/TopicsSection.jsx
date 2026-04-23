import { useDispatch, useSelector } from "react-redux";
import { setField } from "../../store/formSlice";

export default function TopicsSection() {
  const dispatch = useDispatch();
  const { topics_discussed } = useSelector((s) => s.form);

  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-1">Topics Discussed</label>
      <textarea
        value={topics_discussed}
        onChange={(e) => dispatch(setField({ field: "topics_discussed", value: e.target.value }))}
        placeholder="Enter key discussion points..."
        rows={4}
        className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400 resize-none"
      />
      <button className="mt-1 text-xs text-blue-600 flex items-center gap-1 hover:text-blue-800">
        🎤 Summarize from Voice Note (Requires Consent)
      </button>
    </div>
  );
}
