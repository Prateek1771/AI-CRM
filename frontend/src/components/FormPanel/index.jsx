import InteractionDetails from "./InteractionDetails";
import TopicsSection from "./TopicsSection";
import MaterialsSection from "./MaterialsSection";
import SentimentSelector from "./SentimentSelector";
import OutcomesSection from "./OutcomesSection";
import FollowUpSection from "./FollowUpSection";
import FormActions from "./FormActions";

export default function FormPanel() {
  return (
    <div className="h-full overflow-y-auto p-6 space-y-6">
      <InteractionDetails />
      <TopicsSection />
      <MaterialsSection />
      <SentimentSelector />
      <OutcomesSection />
      <FollowUpSection />
      <FormActions />
    </div>
  );
}
