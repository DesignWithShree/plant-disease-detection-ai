import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setImage(file);
    setPreview(URL.createObjectURL(file));
    setResult(null);
  };

  const handlePredict = async () => {
    if (!image) return alert("Upload image first");

    const formData = new FormData();
    formData.append("file", image);

    try {
      setLoading(true);
      const res = await axios.post("http://127.0.0.1:8000/predict", formData);
      setResult(res.data);
    } catch (err) {
      alert("Backend error");
    } finally {
      setLoading(false);
    }
  };

  const formatLabel = (label) =>
    label ? label.replace("___", " - ").replace(/_/g, " ") : "Unknown";

  return (
    <div className="layout">

      {/* SIDEBAR */}
      <div className="sidebar">
        <h2>🌿 AgriAI</h2>
        <p>Plant Disease Detector</p>
      </div>

      {/* MAIN CONTENT */}
      <div className="main">

        <div className="top">
          <h1>Plant Disease Analysis</h1>
          <p>Upload a leaf image to detect disease using AI</p>
        </div>

        {/* Upload Section */}
        <div className="upload-box">
          <input type="file" onChange={handleUpload} />

          {preview && (
            <img src={preview} alt="preview" className="preview" />
          )}

          <button onClick={handlePredict}>
            {loading ? "Analyzing..." : "Analyze Image"}
          </button>
        </div>

        {/* RESULT */}
        {result && (
          <div className="result-box">

            <h2>🌱 {formatLabel(result.prediction)}</h2>
            <p className="confidence">
              Confidence: {(result.confidence * 100).toFixed(1)}%
            </p>

            {/* INFO */}
            <div className="info-grid">
              <div>
                <h4>Plant</h4>
                <p>{result.rag_analysis?.plant}</p>
              </div>

              <div>
                <h4>Disease</h4>
                <p>{result.rag_analysis?.disease}</p>
              </div>

              <div>
                <h4>Severity</h4>
                <p>{result.rag_analysis?.severity}</p>
              </div>
            </div>

            {/* AI EXPLANATION */}
            <div className="ai-section">
              <h3>🤖 AI Explanation</h3>
              <div className="ai-text">
                {result.rag_analysis?.ai_explanation
                  ?.split("\n")
                  .map((line, i) => (
                    <p key={i}>{line}</p>
                  ))}
              </div>
            </div>

            {/* SOLUTIONS */}
            <div className="solution-grid">

              <div>
                <h4>Fertilizer</h4>
                <ul>
                  {(result.rag_analysis?.fertilizer || []).map((f, i) => (
                    <li key={i}>{f}</li>
                  ))}
                </ul>
              </div>

              <div>
                <h4>Pesticide</h4>
                <ul>
                  {(result.rag_analysis?.pesticide || []).map((p, i) => (
                    <li key={i}>{p}</li>
                  ))}
                </ul>
              </div>

              <div>
                <h4>Organic</h4>
                <ul>
                  {(result.rag_analysis?.organic_solution || []).map((o, i) => (
                    <li key={i}>{o}</li>
                  ))}
                </ul>
              </div>

              <div>
                <h4>Prevention</h4>
                <ul>
                  {(result.rag_analysis?.prevention || []).map((p, i) => (
                    <li key={i}>{p}</li>
                  ))}
                </ul>
              </div>

            </div>

          </div>
        )}

      </div>
    </div>
  );
}

export default App;