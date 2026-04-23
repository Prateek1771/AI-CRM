import { useDispatch, useSelector } from "react-redux";
import { setField } from "../../store/formSlice";

export default function OutcomesSection() {
  const dispatch = useDispatch();
  const { outcomes } = useSelector((s) => s.form);

  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-1">Outcomes</label>
      <textarea
        value={outcomes}
        onChange={(e) => dispatch(setField({ field: "outcomes", value: e.target.value }))}
        placeholder="Key outcomes or agreements..."
        rows={3}
        className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400 resize-none"
      />
    </div>
  );
}
