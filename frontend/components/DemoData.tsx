"use client";

interface DemoDataProps {
  onLoadDemo: (demoResult: any) => void;
}

export default function DemoData({ onLoadDemo }: DemoDataProps) {
  const demoResults = [
    {
      name: "John Smith - Diabetes Follow-up",
      data: {
        transcript: [
          { speaker: "Doctor", text: "Good morning, John. How have you been feeling since our last visit?" },
          { speaker: "Patient", text: "Hi Dr. Johnson. I'm John Smith. I've been having some issues with my blood sugar levels lately." },
          { speaker: "Doctor", text: "I see. Can you tell me more about what you've been experiencing?" },
          { speaker: "Patient", text: "Well, I've been feeling more tired than usual, and I've noticed I'm getting thirsty more often. My blood sugar readings have been around 180-200 in the mornings." },
          { speaker: "Doctor", text: "That's concerning. Are you still taking your Metformin as prescribed?" },
          { speaker: "Patient", text: "Yes, I take 500mg twice daily as you recommended. But I have to admit, I haven't been as strict with my diet lately." }
        ],
        redaction_summary: ["SSN patterns", "Specific dates"],
        detected_entity_types: ["PERSON", "DATE", "MEDICAL"],
        processing_note: "Phase 1: Audio transcription with speaker identification, PII redaction, and medical record retrieval",
        segments_count: 6,
        patient_identified: true,
        patient_id: "P12345678",
        medical_records: [
          {
            type: "Medical History",
            content: "Patient has a history of Type 2 diabetes diagnosed in 2018. Currently managed with Metformin. Previous HbA1c levels have been well controlled at 6.8-7.2%.",
            date: "2024-01-10T10:30:00Z"
          },
          {
            type: "Current Medications",
            content: "Metformin 500mg twice daily, Lisinopril 10mg daily for blood pressure management.",
            date: "2024-01-10T10:30:00Z"
          },
          {
            type: "Previous Visit",
            content: "Last visit on January 10, 2024: Blood pressure 135/85, HbA1c 7.1%. Patient reported good adherence to medication. Recommended continued diet modification and regular exercise.",
            date: "2024-01-10T10:30:00Z"
          },
          {
            type: "Allergies",
            content: "No known drug allergies. Patient reports mild lactose intolerance.",
            date: "2023-12-15T14:20:00Z"
          }
        ],
        extracted_patient_info: {
          name: "John Smith",
          condition: "diabetes"
        },
        new_medical_info: [
          {
            type: "Current Symptoms",
            content: "Patient reports: increased fatigue and thirst, morning blood glucose 180-200 mg/dL",
            source: "audio_conversation"
          },
          {
            type: "Medication Adherence",
            content: "Patient confirmed: taking Metformin 500mg twice daily as prescribed",
            source: "audio_conversation"
          },
          {
            type: "Lifestyle Factors",
            content: "Patient mentioned: decreased adherence to dietary recommendations",
            source: "audio_conversation"
          }
        ]
      }
    },
    {
      name: "Mary Johnson - Asthma Check-up",
      data: {
        transcript: [
          { speaker: "Doctor", text: "Hello Mary, what brings you in today?" },
          { speaker: "Patient", text: "Hi, I'm Mary Johnson. I've been having some breathing difficulties, especially at night." },
          { speaker: "Doctor", text: "I'm sorry to hear that. Can you describe what the breathing difficulties feel like?" },
          { speaker: "Patient", text: "It feels like I can't get enough air, and I've been using my rescue inhaler more often - maybe 3-4 times this week." },
          { speaker: "Doctor", text: "That's more frequent than we'd like to see. Are you still using your daily controller medication?" },
          { speaker: "Patient", text: "Yes, I use the Flovent inhaler every morning and evening as prescribed." }
        ],
        redaction_summary: ["Personal identifiers"],
        detected_entity_types: ["PERSON", "MEDICAL"],
        processing_note: "Phase 1: Audio transcription with speaker identification, PII redaction, and medical record retrieval",
        segments_count: 6,
        patient_identified: true,
        patient_id: "P87654321",
        medical_records: [
          {
            type: "Medical History",
            content: "Patient diagnosed with moderate persistent asthma in 2019. Well-controlled on combination therapy. No history of severe exacerbations requiring hospitalization.",
            date: "2024-01-05T09:15:00Z"
          },
          {
            type: "Current Medications",
            content: "Fluticasone (Flovent) 110mcg 2 puffs twice daily, Albuterol rescue inhaler as needed.",
            date: "2024-01-05T09:15:00Z"
          },
          {
            type: "Previous Visit",
            content: "Last visit on January 5, 2024: Respiratory function normal, peak flow 380 L/min. Patient reported good control with minimal rescue inhaler use.",
            date: "2024-01-05T09:15:00Z"
          }
        ],
        extracted_patient_info: {
          name: "Mary Johnson",
          condition: "asthma"
        },
        new_medical_info: [
          {
            type: "Current Symptoms",
            content: "Patient reports: nocturnal breathing difficulties, increased rescue inhaler use (3-4 times this week)",
            source: "audio_conversation"
          },
          {
            type: "Medication Adherence",
            content: "Patient confirmed: using Flovent inhaler twice daily as prescribed",
            source: "audio_conversation"
          }
        ]
      }
    }
  ];

  return (
    <div className="bg-blue-50 border border-blue-200 rounded-xl p-4 mb-6">
      <h3 className="font-medium text-blue-800 mb-3 flex items-center">
        <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
          <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        Demo Mode - Try Sample Data
      </h3>
      <p className="text-sm text-blue-600 mb-4">
        Experience the system with realistic medical consultation examples
      </p>
      <div className="space-y-2">
        {demoResults.map((demo, index) => (
          <button
            key={index}
            onClick={() => onLoadDemo(demo.data)}
            className="w-full text-left px-3 py-2 bg-white border border-blue-200 rounded-lg hover:bg-blue-50 transition-colors text-sm"
          >
            <div className="font-medium text-blue-800">{demo.name}</div>
            <div className="text-blue-600 text-xs">
              {demo.data.transcript.length} segments • Patient ID: {demo.data.patient_id}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}