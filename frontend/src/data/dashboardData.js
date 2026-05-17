export const modelMetrics = [
  {
    label: "Accuracy",
    value: "97.10%",
    description: "Overall correctly identified records across all classes.",
  },
  {
    label: "Precision",
    value: "74.10%",
    description: "True malicious detections among all predicted threats.",
  },
  {
    label: "Recall",
    value: "71.03%",
    description: "The system’s ability to find actual malicious activities.",
  },
  {
    label: "F1-Score",
    value: "72.53%",
    description: "Balanced evaluation of precision and recall.",
  },
];

export const pipelineSteps = [
  {
    number: 1,
    title: "Upload CSV",
    description: "Import employee behavioural records for analysis.",
  },
  {
    number: 2,
    title: "Validate Data",
    description: "Check required columns and remove unnecessary fields.",
  },
  {
    number: 3,
    title: "Predict Behaviour",
    description: "Apply the trained Random Forest classification model.",
  },
  {
    number: 4,
    title: "Explain Result",
    description: "Generate confidence, risk level, and readable explanation.",
  },
];

export const indicators = [
  { label: "Off-hours Printing", icon: "print" },
  { label: "Total Printed Pages", icon: "description" },
  { label: "File Burning Activity", icon: "local_fire_department" },
  { label: "Files Burned From Other Source", icon: "folder_zip" },
  { label: "Weekend Facility Entry", icon: "event" },
  { label: "Number of Facility Entries", icon: "login" },
  { label: "Campus Access", icon: "corporate_fare" },
  { label: "Number of Unique Campuses Accessed", icon: "apartment" },
  { label: "Activity While Abroad", icon: "public" },
  { label: "Trip Day Number", icon: "calendar_today" },
  { label: "Hostility Country Level", icon: "warning" },
  { label: "Contractor Status", icon: "badge" },
  { label: "Employee Classification", icon: "groups" },
];

export const testingExamples = [
  {
    type: "TRUE POSITIVE",
    confidence: "98%",
    badgeClass: "bg-[#ba1a1a]/10 text-[#ba1a1a] border-[#ba1a1a]/20",
    description:
      "Successful detection of actual malicious activity. High-severity alert triggered.",
  },
  {
    type: "TRUE NEGATIVE",
    confidence: "98%",
    badgeClass: "bg-[#d5e3fd] text-[#3a485c] border-[#c6c6cd]",
    description:
      "Correctly identified standard, non-malicious business operations.",
  },
  {
    type: "FALSE POSITIVE",
    confidence: "61%",
    badgeClass: "bg-[#eceef0] text-[#515f74] border-[#c6c6cd]",
    description:
      "Benign activity misclassified as a threat. This requires human review.",
  },
  {
    type: "FALSE NEGATIVE",
    confidence: "86%",
    badgeClass: "bg-[#ffdad6] text-[#93000a] border-[#ba1a1a]/20",
    description:
      "Failure to detect actual malicious activity. This is a critical limitation.",
  },
];

export const confusionMatrix = {
  trueNormal: "22,129",
  falsePositive: "317",
  falseNegative: "370",
  trueMalicious: "907",
};

export const interpretabilityFeatures = [
  {
    label: "File Burning Activity",
    impact: "+42% Impact",
    width: "42%",
  },
  {
    label: "Off-hours Printing",
    impact: "+28% Impact",
    width: "28%",
  },
  {
    label: "Total Printed Pages",
    impact: "+15% Impact",
    width: "15%",
  },
];