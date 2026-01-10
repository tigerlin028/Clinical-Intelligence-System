"use client";

export default function Home() {
  const sendTest = async () => {
    console.log("Sending test request...");

    try {
      const res = await fetch("https://ingestion-service-523658399118.us-central1.run.app/ingest", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: "hello from frontend",
        }),
      });

      const data = await res.json();
      console.log("Response from backend:", data);
    } catch (err) {
      console.error("Request failed:", err);
    }
  };

  return (
    <main style={{ padding: "40px" }}>
      <h1>Clinical Ambient Intelligence</h1>
      <p>Phase 1 – Feature 1</p>
      <button onClick={sendTest}>Send Test</button>
    </main>
  );
}
