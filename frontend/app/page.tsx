"use client";
import { useState } from "react";

export default function Home() {
  const [response, setResponse] = useState<string | null>(null);

  const sendTest = async () => {
    console.log("Sending test request...");

    try {
      const res = await fetch("https://ingestion-service-523658399118.us-central1.run.app/ingest", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: "Hello, my name is John Smith. My SSN is 123-45-6789.",
        }),
      });

      const data = await res.json();
      setResponse(data.result.processed_text);
    } catch (err) {
      console.error("Request failed:", err);
    }
  };

  return (
    <main style={{ padding: "40px" }}>
      <h1>Clinical Ambient Intelligence</h1>
      <p>Phase 1 – Feature 1</p>
      <button onClick={sendTest}>Send Test</button>

      {response && (
        <div style={{ marginTop: "20px", fontWeight: "bold" }}>
          Response: {response}
        </div>
      )}
    </main>
  );
}
