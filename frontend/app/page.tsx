"use client";
import { useState } from "react";

export default function AudioUploadDemo() {
  const [transcript, setTranscript] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const uploadAudio = async (file: File) => {
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch(
      "https://ingestion-service-xxxxx.us-central1.run.app/upload-audio",
      {
        method: "POST",
        body: formData,
      }
    );

    const data = await res.json();
    setTranscript(data.transcript);
    setLoading(false);
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Clinical Audio Upload (Demo)</h2>

      <input
        type="file"
        accept="audio/*"
        onChange={(e) => {
          if (e.target.files?.[0]) {
            uploadAudio(e.target.files[0]);
          }
        }}
      />

      {loading && <p>Processing audio…</p>}

      <ul>
        {transcript.map((seg, i) => (
          <li key={i}>
            <b>{seg.speaker}:</b> {seg.text}
          </li>
        ))}
      </ul>
    </div>
  );
}
