"use client";

import { useState } from "react";

export default function Home() {
  const [inputText, setInputText] = useState("");
  const [response, setResponse] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const sendTest = async () => {
    setLoading(true);
    setResponse(null);

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
      setResponse(data.result.redacted_text);
    } catch (err) {
      console.error("Request failed:", err);
      setResponse("Request failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main style={{ padding: "40px", maxWidth: "600px" }}>
      <h1>Clinical Ambient Intelligence</h1>
      <p>Feature 4 – PII / PHI Redaction</p>

      <textarea
        rows={4}
        style={{ width: "100%", marginBottom: "12px" }}
        placeholder="Enter text with PII (e.g. SSN, name, date)"
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
      />

      <button onClick={sendTest} disabled={loading || !inputText}>
        {loading ? "Processing..." : "Send Test"}
      </button>

      {response && (
        <div
          style={{
            marginTop: "20px",
            padding: "12px",
            border: "1px solid #ccc",
            background: "#f9f9f9",
            fontWeight: "bold",
          }}
        >
          Redacted Output:
          <div style={{ marginTop: "8px" }}>{response}</div>
        </div>
      )}
    </main>
  );
}
