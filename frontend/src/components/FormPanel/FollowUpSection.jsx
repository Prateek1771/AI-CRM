import { useDispatch, useSelector } from "react-redux";
import { setField } from "../../store/formSlice";

export default function FollowUpSection() {
  const dispatch = useDispatch();
  const { follow_up_actions, follow_up_date } = useSelector((s) => s.form);

  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-1">Follow-up Actions</label>
      <div className="grid grid-cols-2 gap-3">
        <input
          value={follow_up_actions}
          onChange={(e) => dispatch(setField({ field: "follow_up_actions", value: e.target.value }))}
          placeholder="Schedule follow-up, send materials..."
          className="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
        <input
          type="date"
          value={follow_up_date || ""}
          onChange={(e) => dispatch(setField({ field: "follow_up_date", value: e.target.value }))}
          className="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
      </div>
    </div>
  );
}
