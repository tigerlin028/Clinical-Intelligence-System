"use client";
import { useState } from "react";
import { API_URL } from "../lib/config";

interface TranscriptSegment {
  speaker: string;
  text: string;
}

interface MedicalRecord {
  type: string;
  content: string;
  date: string;
  metadata?: any;
}

interface ProcessingResult {
  transcript: TranscriptSegment[];
  redaction_summary?: string[];
  detected_entity_types?: string[];
  processing_note?: string;
  segments_count?: number;
  // RAG系统相关字段
  patient_identified?: boolean;
  patient_id?: string;
  medical_records?: MedicalRecord[];
  extracted_patient_info?: Record<string, string>;
  new_medical_info?: Array<{type: string; content: string; source: string}>;
  rag_error?: string;
}

export default function AudioUploadDemo() {
  const [result, setResult] = useState<ProcessingResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const uploadAudio = async (file: File) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch(
        `${API_URL}/upload-audio`,
        {
          method: "POST",
          body: formData,
        }
      );

      if (!res.ok) {
        throw new Error(`Upload failed: ${res.status} ${res.statusText}`);
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h1 className="text-2xl font-bold text-gray-800 mb-6">
          Clinical Intelligence System - Phase 1 Demo
        </h1>
        
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Upload Audio File
          </label>
          <input
            type="file"
            accept="audio/*"
            onChange={(e) => {
              if (e.target.files?.[0]) {
                uploadAudio(e.target.files[0]);
              }
            }}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
            disabled={loading}
          />
        </div>

        {loading && (
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <span className="ml-3 text-gray-600">Processing audio with PII redaction...</span>
          </div>
        )}

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-md p-4 mb-6">
            <div className="text-red-800">
              <strong>Error:</strong> {error}
            </div>
          </div>
        )}

        {result && (
          <div className="space-y-6">
            {/* Privacy Notice */}
            <div className="bg-green-50 border border-green-200 rounded-md p-4">
              <div className="text-green-800">
                <strong>✓ Privacy Protected:</strong> All sensitive information has been automatically redacted
                {result.redaction_summary && result.redaction_summary.length > 0 && (
                  <span className="ml-2">
                    (Detected: {result.redaction_summary.join(", ")})
                  </span>
                )}
              </div>
            </div>

            {/* Patient Identification Status */}
            {result.patient_identified ? (
              <div className="bg-blue-50 border border-blue-200 rounded-md p-4">
                <div className="text-blue-800">
                  <strong>✓ Patient Identified:</strong> {result.patient_id}
                  {result.extracted_patient_info && Object.keys(result.extracted_patient_info).length > 0 && (
                    <div className="mt-2 text-sm">
                      <strong>Extracted Info:</strong> {Object.entries(result.extracted_patient_info).map(([key, value]) => `${key}: ${value}`).join(", ")}
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <div className="bg-yellow-50 border border-yellow-200 rounded-md p-4">
                <div className="text-yellow-800">
                  <strong>⚠ Patient Not Identified:</strong> {result.rag_error || "Unable to match patient information"}
                </div>
              </div>
            )}

            {/* New Medical Information Extracted */}
            {result.new_medical_info && result.new_medical_info.length > 0 && (
              <div className="bg-green-50 border border-green-200 rounded-md p-4">
                <div className="text-green-800">
                  <strong>✓ New Medical Information Extracted:</strong>
                  <ul className="mt-2 list-disc list-inside">
                    {result.new_medical_info.map((info, i) => (
                      <li key={i} className="text-sm">
                        <strong>{info.type}:</strong> {info.content}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            )}

            {/* Medical Records */}
            {result.medical_records && result.medical_records.length > 0 && (
              <div>
                <h2 className="text-lg font-semibold text-gray-800 mb-4">
                  Medical Records ({result.patient_id})
                </h2>
                <div className="space-y-3">
                  {result.medical_records.map((record, i) => (
                    <div key={i} className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                      <div className="flex justify-between items-start mb-2">
                        <span className="inline-block px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                          {record.type}
                        </span>
                        <span className="text-sm text-gray-500">
                          {new Date(record.date).toLocaleDateString()}
                        </span>
                      </div>
                      <p className="text-gray-700">{record.content}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Transcript */}
            <div>
              <h2 className="text-lg font-semibold text-gray-800 mb-4">
                Transcript with Speaker Identification
              </h2>
              <div className="bg-gray-50 rounded-lg p-4 space-y-3">
                {result.transcript.map((seg, i) => (
                  <div key={i} className="flex">
                    <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium mr-3 ${
                      seg.speaker === 'Doctor' 
                        ? 'bg-blue-100 text-blue-800' 
                        : 'bg-green-100 text-green-800'
                    }`}>
                      {seg.speaker}
                    </span>
                    <span className="text-gray-700 flex-1">{seg.text}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Technical Details */}
            {result.detected_entity_types && result.detected_entity_types.length > 0 && (
              <details className="text-sm text-gray-600">
                <summary className="cursor-pointer font-medium">Technical Details</summary>
                <div className="mt-2 pl-4">
                  <p>Semantic PII Detection: {result.detected_entity_types.join(", ")}</p>
                  <p>Processing: {result.processing_note}</p>
                  {result.segments_count && <p>Audio Segments: {result.segments_count}</p>}
                </div>
              </details>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
