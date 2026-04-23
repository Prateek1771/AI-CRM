import { useDispatch, useSelector } from "react-redux";
import { clearAiHighlight } from "../../store/formSlice";

export default function MaterialsSection() {
  const dispatch = useDispatch();
  const { materials_shared, samples_distributed, aiPopulatedFields } = useSelector((s) => s.form);

  return (
    <div className="space-y-3">
      <h3 className="text-sm font-medium text-gray-700">Materials Shared / Samples Distributed</h3>
      <div>
        <div className="text-xs font-medium text-gray-500 mb-1">Materials Shared</div>
        <div className="flex items-center gap-2">
          <div
            className={`flex-1 text-sm text-gray-600 min-h-[2rem] px-3 py-1.5 border border-gray-200 rounded-md bg-gray-50 ${aiPopulatedFields.includes("materials_shared") ? "ai-populated" : ""}`}
            onAnimationEnd={() => dispatch(clearAiHighlight("materials_shared"))}
          >
            {materials_shared.length ? materials_shared.join(", ") : <span className="text-gray-400">Brochures, studies...</span>}
          </div>
          <button className="text-xs border border-gray-300 rounded px-2 py-1 hover:bg-gray-50 whitespace-nowrap">🔍 Search/Add</button>
        </div>
      </div>
      <div>
        <div className="text-xs font-medium text-gray-500 mb-1">Samples Distributed</div>
        <div className="flex items-center gap-2">
          <div
            className={`flex-1 text-sm min-h-[2rem] px-3 py-1.5 border border-gray-200 rounded-md bg-gray-50 ${aiPopulatedFields.includes("samples_distributed") ? "ai-populated" : ""}`}
            onAnimationEnd={() => dispatch(clearAiHighlight("samples_distributed"))}
          >
            {samples_distributed.length ? <span className="text-gray-600">{samples_distributed.join(", ")}</span> : <span className="text-gray-400">No samples added.</span>}
          </div>
          <button className="text-xs border border-gray-300 rounded px-2 py-1 hover:bg-gray-50 whitespace-nowrap">+ Add Sample</button>
        </div>
      </div>
    </div>
  );
}
