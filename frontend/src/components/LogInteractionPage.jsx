import FormPanel from "./FormPanel";
import AIAssistantPanel from "./AIAssistantPanel";

export default function LogInteractionPage() {
  return (
    <div className="flex h-screen bg-gray-50 font-sans">
      <div className="flex-1 min-w-0">
        <FormPanel />
      </div>
      <div className="w-96 flex-shrink-0">
        <AIAssistantPanel />
      </div>
    </div>
  );
}
