"use client";

import { useState } from "react";

export default function Home() {
  const [inputText, setInputText] = useState("");
  const [responseText, setResponseText] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const sendTest = async () => {
    if (!inputText.trim()) return;

    setLoading(true);
    setResponseText(null);

    try {
      const res = await fetch(
        "https://ingestion-service-523658399118.us-central1.run.app/ingest",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            text: inputText,
          }),
        }
      );

      const data = await res.json();

      // ⚠️ Feature 4 核心原则：前端只用 redacted_text
      setResponseText(data.result.redacted_text);
    } catch (err) {
      console.error("Request failed:", err);
      setResponseText("Error processing input.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main style={{ padding: "40px", maxWidth: "700px" }}>
      <h1>Clinical Ambient Intelligence</h1>
      <p>Phase 1 – Feature 4 (PII / PHI Redaction)</p>

      {/* 用户输入区域 */}
      <textarea
        rows={5}
        style={{ width: "100%", padding: "10px", fontSize: "14px" }}
        placeholder="Enter clinical text here..."
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
      />

      <button
        onClick={sendTest}
        disabled={loading}
        style={{ marginTop: "12px" }}
      >
        {loading ? "Processing..." : "Redact PII"}
      </button>

      {/* 输出区域 */}
      {responseText && (
        <div
          style={{
            marginTop: "20px",
            padding: "12px",
            border: "1px solid #ccc",
            backgroundColor: "#f9f9f9",
            whiteSpace: "pre-wrap",
          }}
        >
          <strong>Redacted Output:</strong>
          <div>{responseText}</div>
        </div>
      )}
    </main>
  );
}
