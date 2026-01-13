"use client";
import { useState } from "react";
import { API_URL } from "../lib/config";

interface TranscriptSegment {
  speaker: string;
  text: string;
}

interface MedicalRecord {
  id?: number;  // 添加ID字段
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
  const [dragActive, setDragActive] = useState(false);
  const [deleteConfirm, setDeleteConfirm] = useState<{show: boolean; recordId: number | null; recordContent: string}>({
    show: false,
    recordId: null,
    recordContent: ''
  });
  const [deleting, setDeleting] = useState(false);

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

  const handleDeleteRecord = (recordId: number, recordContent: string) => {
    setDeleteConfirm({
      show: true,
      recordId,
      recordContent
    });
  };

  const confirmDelete = async () => {
    if (!deleteConfirm.recordId) return;

    setDeleting(true);
    try {
      const res = await fetch(`${API_URL}/medical-record/${deleteConfirm.recordId}`, {
        method: 'DELETE',
      });

      if (!res.ok) {
        throw new Error('Failed to delete record');
      }

      // 从当前结果中移除已删除的记录
      if (result && result.medical_records) {
        const updatedRecords = result.medical_records.filter(record => record.id !== deleteConfirm.recordId);
        setResult({
          ...result,
          medical_records: updatedRecords
        });
      }

      setDeleteConfirm({ show: false, recordId: null, recordContent: '' });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete record");
    } finally {
      setDeleting(false);
    }
  };

  const cancelDelete = () => {
    setDeleteConfirm({ show: false, recordId: null, recordContent: '' });
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      uploadAudio(e.dataTransfer.files[0]);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Header */}
      <div className="medical-gradient text-white py-8">
        <div className="max-w-6xl mx-auto px-6">
          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 bg-white/20 rounded-lg flex items-center justify-center">
              <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <div>
              <h1 className="text-3xl font-bold">Clinical Intelligence System</h1>
              <p className="text-blue-100 mt-1">AI-Powered Ambient Intelligence for Medical Consultations</p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Upload Section */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl card-shadow-lg p-6 sticky top-8">
              <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
                <svg className="w-5 h-5 mr-2 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"/>
                </svg>
                Audio Upload
              </h2>
              
              <div
                className={`border-2 border-dashed rounded-lg p-8 text-center transition-all duration-200 ${
                  dragActive 
                    ? 'border-blue-400 bg-blue-50' 
                    : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'
                } ${loading ? 'opacity-50 pointer-events-none' : ''}`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
              >
                <svg className="mx-auto h-12 w-12 text-gray-400 mb-4" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                  <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                <p className="text-gray-600 mb-2">
                  {dragActive ? 'Drop your audio file here' : 'Drag & drop your audio file here'}
                </p>
                <p className="text-sm text-gray-500 mb-4">or</p>
                <input
                  type="file"
                  accept="audio/*"
                  onChange={(e) => {
                    if (e.target.files?.[0]) {
                      uploadAudio(e.target.files[0]);
                    }
                  }}
                  className="hidden"
                  id="audio-upload"
                  disabled={loading}
                />
                <label
                  htmlFor="audio-upload"
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 cursor-pointer transition-colors"
                >
                  Choose File
                </label>
              </div>

              {/* Processing Status */}
              {loading && (
                <div className="mt-6 animate-fade-in">
                  <div className="flex items-center justify-center py-4">
                    <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
                    <span className="ml-3 text-gray-600 text-sm">Processing audio...</span>
                  </div>
                  <div className="bg-blue-50 rounded-lg p-4 mt-4">
                    <div className="text-sm text-blue-800">
                      <div className="flex items-center mb-2">
                        <div className="animate-pulse-slow w-2 h-2 bg-blue-600 rounded-full mr-2"></div>
                        Transcribing speech to text
                      </div>
                      <div className="flex items-center mb-2">
                        <div className="animate-pulse-slow w-2 h-2 bg-blue-600 rounded-full mr-2" style={{animationDelay: '0.5s'}}></div>
                        Identifying speakers
                      </div>
                      <div className="flex items-center mb-2">
                        <div className="animate-pulse-slow w-2 h-2 bg-blue-600 rounded-full mr-2" style={{animationDelay: '1s'}}></div>
                        Redacting sensitive information
                      </div>
                      <div className="flex items-center">
                        <div className="animate-pulse-slow w-2 h-2 bg-blue-600 rounded-full mr-2" style={{animationDelay: '1.5s'}}></div>
                        Retrieving medical records
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Features List */}
              <div className="mt-8 space-y-3">
                <h3 className="font-medium text-gray-800">Features</h3>
                <div className="space-y-2 text-sm text-gray-600">
                  <div className="flex items-center">
                    <svg className="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd"/>
                    </svg>
                    Real-time transcription
                  </div>
                  <div className="flex items-center">
                    <svg className="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd"/>
                    </svg>
                    Speaker identification
                  </div>
                  <div className="flex items-center">
                    <svg className="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd"/>
                    </svg>
                    PII/PHI protection
                  </div>
                  <div className="flex items-center">
                    <svg className="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd"/>
                    </svg>
                    Medical record retrieval
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Results Section */}
          <div className="lg:col-span-2">
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-xl p-6 mb-6 animate-fade-in">
                <div className="flex items-center">
                  <svg className="w-5 h-5 text-red-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd"/>
                  </svg>
                  <div>
                    <strong className="text-red-800">Error:</strong>
                    <span className="text-red-700 ml-1">{error}</span>
                  </div>
                </div>
              </div>
            )}

            {result && (
              <div className="space-y-6 animate-fade-in">
                {/* Status Cards */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {/* Privacy Status */}
                  <div className="bg-green-50 border border-green-200 rounded-xl p-4">
                    <div className="flex items-center">
                      <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center mr-3">
                        <svg className="w-4 h-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/>
                        </svg>
                      </div>
                      <div>
                        <div className="font-medium text-green-800">Privacy Protected</div>
                        <div className="text-sm text-green-600">
                          {result.redaction_summary && result.redaction_summary.length > 0 
                            ? `Redacted: ${result.redaction_summary.join(", ")}`
                            : "All sensitive data secured"
                          }
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Patient Status */}
                  <div className={`${result.patient_identified ? 'bg-blue-50 border-blue-200' : 'bg-yellow-50 border-yellow-200'} border rounded-xl p-4`}>
                    <div className="flex items-center">
                      <div className={`w-8 h-8 ${result.patient_identified ? 'bg-blue-100' : 'bg-yellow-100'} rounded-full flex items-center justify-center mr-3`}>
                        <svg className={`w-4 h-4 ${result.patient_identified ? 'text-blue-600' : 'text-yellow-600'}`} fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd"/>
                        </svg>
                      </div>
                      <div>
                        <div className={`font-medium ${result.patient_identified ? 'text-blue-800' : 'text-yellow-800'}`}>
                          {result.patient_identified ? 'Patient Identified' : 'Patient Not Found'}
                        </div>
                        <div className={`text-sm ${result.patient_identified ? 'text-blue-600' : 'text-yellow-600'}`}>
                          {result.patient_identified ? result.patient_id : 'Unable to match records'}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Medical Records */}
                {result.medical_records && result.medical_records.length > 0 && (
                  <div className="bg-white rounded-xl card-shadow p-6">
                    <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
                      <svg className="w-5 h-5 mr-2 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M4 4a2 2 0 00-2 2v8a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2H4zm0 2h12v8H4V6z"/>
                      </svg>
                      Medical Records ({result.patient_id})
                    </h2>
                    <div className="grid gap-4">
                      {result.medical_records.map((record, i) => (
                        <div key={i} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow group">
                          <div className="flex justify-between items-start mb-3">
                            <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                              {record.type}
                            </span>
                            <div className="flex items-center space-x-2">
                              <span className="text-sm text-gray-500">
                                {new Date(record.date).toLocaleDateString()}
                              </span>
                              {record.id && (
                                <button
                                  onClick={() => handleDeleteRecord(record.id!, record.content)}
                                  className="opacity-0 group-hover:opacity-100 transition-opacity p-1 text-red-500 hover:text-red-700 hover:bg-red-50 rounded"
                                  title="Delete this record"
                                >
                                  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                                    <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd"/>
                                  </svg>
                                </button>
                              )}
                            </div>
                          </div>
                          <p className="text-gray-700 leading-relaxed">{record.content}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* New Medical Information */}
                {result.new_medical_info && result.new_medical_info.length > 0 && (
                  <div className="bg-white rounded-xl card-shadow p-6">
                    <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
                      <svg className="w-5 h-5 mr-2 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V7z" clipRule="evenodd"/>
                      </svg>
                      New Medical Information Extracted
                    </h2>
                    <div className="space-y-3">
                      {result.new_medical_info.map((info, i) => (
                        <div key={i} className="bg-green-50 border border-green-200 rounded-lg p-4">
                          <div className="flex items-start">
                            <span className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-green-100 text-green-800 mr-3">
                              {info.type}
                            </span>
                            <p className="text-gray-700 flex-1">{info.content}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Transcript */}
                <div className="bg-white rounded-xl card-shadow p-6">
                  <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
                    <svg className="w-5 h-5 mr-2 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" clipRule="evenodd"/>
                    </svg>
                    Conversation Transcript
                  </h2>
                  <div className="space-y-4 max-h-96 overflow-y-auto">
                    {result.transcript.map((seg, i) => (
                      <div key={i} className="flex items-start space-x-3">
                        <div className={`flex-shrink-0 w-20 text-center py-2 px-3 rounded-lg text-sm font-medium ${
                          seg.speaker === 'Doctor' 
                            ? 'bg-blue-100 text-blue-800' 
                            : 'bg-green-100 text-green-800'
                        }`}>
                          {seg.speaker}
                        </div>
                        <div className="flex-1 bg-gray-50 rounded-lg p-3">
                          <p className="text-gray-700 leading-relaxed">{seg.text}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Technical Details */}
                {result.detected_entity_types && result.detected_entity_types.length > 0 && (
                  <details className="bg-gray-50 rounded-xl p-4">
                    <summary className="cursor-pointer font-medium text-gray-700 hover:text-gray-900">
                      Technical Processing Details
                    </summary>
                    <div className="mt-4 text-sm text-gray-600 space-y-2">
                      <div className="flex justify-between">
                        <span>PII Detection:</span>
                        <span className="font-mono">{result.detected_entity_types.join(", ")}</span>
                      </div>
                      {result.segments_count && (
                        <div className="flex justify-between">
                          <span>Audio Segments:</span>
                          <span className="font-mono">{result.segments_count}</span>
                        </div>
                      )}
                      <div className="text-xs text-gray-500 mt-2">
                        {result.processing_note}
                      </div>
                    </div>
                  </details>
                )}
              </div>
            )}

            {/* Empty State */}
            {!result && !loading && !error && (
              <div className="bg-white rounded-xl card-shadow p-12 text-center">
                <svg className="mx-auto h-16 w-16 text-gray-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/>
                </svg>
                <h3 className="text-lg font-medium text-gray-900 mb-2">Ready to Process Audio</h3>
                <p className="text-gray-500">Upload an audio file to see AI-powered transcription, speaker identification, and medical record integration in action.</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Delete Confirmation Modal */}
      {deleteConfirm.show && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-6 max-w-md w-full mx-4 animate-fade-in">
            <div className="flex items-center mb-4">
              <div className="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center mr-3">
                <svg className="w-5 h-5 text-red-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd"/>
                </svg>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900">Delete Medical Record</h3>
                <p className="text-sm text-gray-600">This action cannot be undone</p>
              </div>
            </div>
            
            <div className="mb-4">
              <p className="text-sm text-gray-700 mb-2">Are you sure you want to delete this record?</p>
              <div className="bg-gray-50 rounded-lg p-3 max-h-32 overflow-y-auto">
                <p className="text-sm text-gray-600 italic">"{deleteConfirm.recordContent}"</p>
              </div>
            </div>

            <div className="flex justify-end space-x-3">
              <button
                onClick={cancelDelete}
                disabled={deleting}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors disabled:opacity-50"
              >
                Cancel
              </button>
              <button
                onClick={confirmDelete}
                disabled={deleting}
                className="px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-lg transition-colors disabled:opacity-50 flex items-center"
              >
                {deleting ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Deleting...
                  </>
                ) : (
                  'Delete Record'
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
