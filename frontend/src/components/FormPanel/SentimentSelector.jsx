import { useDispatch, useSelector } from "react-redux";
import { setField } from "../../store/formSlice";

const OPTIONS = [
  { value: "positive", label: "Positive", emoji: "😊" },
  { value: "neutral", label: "Neutral", emoji: "😐" },
  { value: "negative", label: "Negative", emoji: "😟" },
];

export default function SentimentSelector() {
  const dispatch = useDispatch();
  const { sentiment } = useSelector((s) => s.form);

  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-2">Observed/Inferred HCP Sentiment</label>
      <div className="flex gap-6">
        {OPTIONS.map((opt) => (
          <label key={opt.value} className="flex items-center gap-2 cursor-pointer">
            <input
              type="radio"
              name="sentiment"
              value={opt.value}
              checked={sentiment === opt.value}
              onChange={() => dispatch(setField({ field: "sentiment", value: opt.value }))}
              className="accent-blue-600"
            />
            <span className="text-sm">{opt.emoji} {opt.label}</span>
          </label>
        ))}
      </div>
    </div>
  );
}
