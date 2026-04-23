import { useDispatch, useSelector } from "react-redux";
import { setField, clearAiHighlight } from "../../store/formSlice";
import client from "../../api/client";
import { useState } from "react";

export default function InteractionDetails() {
  const dispatch = useDispatch();
  const { hcp_name, interaction_type, date, time, attendees, aiPopulatedFields } = useSelector((s) => s.form);
  const [hcpSuggestions, setHcpSuggestions] = useState([]);

  const ai = (field) => aiPopulatedFields.includes(field) ? "ai-populated" : "";

  const handleHcpSearch = async (query) => {
    dispatch(setField({ field: "hcp_name", value: query }));
    if (query.length < 2) { setHcpSuggestions([]); return; }
    try {
      const res = await client.get(`/api/hcps?q=${query}`);
      setHcpSuggestions(res.data);
    } catch {
      setHcpSuggestions([]);
    }
  };

  const selectHcp = (hcp) => {
    dispatch(setField({ field: "hcp_name", value: hcp.name }));
    dispatch(setField({ field: "hcp_id", value: hcp.id }));
    setHcpSuggestions([]);
  };

  return (
    <div className="space-y-4">
      <h2 className="text-xs font-semibold text-gray-500 uppercase tracking-wide">Interaction Details</h2>
      <div className="grid grid-cols-2 gap-4">
        <div className="relative">
          <label className="block text-sm font-medium text-gray-700 mb-1">HCP Name</label>
          <input
            value={hcp_name}
            onChange={(e) => handleHcpSearch(e.target.value)}
            placeholder="Search or select HCP..."
            className={`w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400 ${ai("hcp_name")}`}
            onAnimationEnd={() => dispatch(clearAiHighlight("hcp_name"))}
          />
          {hcpSuggestions.length > 0 && (
            <ul className="absolute z-10 bg-white border border-gray-200 rounded-md w-full mt-1 shadow-sm">
              {hcpSuggestions.map((h) => (
                <li key={h.id} onClick={() => selectHcp(h)} className="px-3 py-2 text-sm cursor-pointer hover:bg-gray-50">
                  {h.name} {h.specialty && <span className="text-gray-400">· {h.specialty}</span>}
                </li>
              ))}
            </ul>
          )}
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Interaction Type</label>
          <select
            value={interaction_type}
            onChange={(e) => dispatch(setField({ field: "interaction_type", value: e.target.value }))}
            className={`w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400 ${ai("interaction_type")}`}
            onAnimationEnd={() => dispatch(clearAiHighlight("interaction_type"))}
          >
            {["Meeting", "Call", "Email", "Conference", "Webinar"].map((t) => (
              <option key={t}>{t}</option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Date</label>
          <input type="date" value={date}
            onChange={(e) => dispatch(setField({ field: "date", value: e.target.value }))}
            className={`w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400 ${ai("date")}`}
            onAnimationEnd={() => dispatch(clearAiHighlight("date"))}
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Time</label>
          <input type="time" value={time}
            onChange={(e) => dispatch(setField({ field: "time", value: e.target.value }))}
            className={`w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400 ${ai("time")}`}
            onAnimationEnd={() => dispatch(clearAiHighlight("time"))}
          />
        </div>
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Attendees</label>
        <input
          value={attendees.join(", ")}
          onChange={(e) => dispatch(setField({ field: "attendees", value: e.target.value.split(",").map(s => s.trim()).filter(Boolean) }))}
          placeholder="Enter names separated by commas..."
          className={`w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400 ${ai("attendees")}`}
          onAnimationEnd={() => dispatch(clearAiHighlight("attendees"))}
        />
      </div>
    </div>
  );
}
