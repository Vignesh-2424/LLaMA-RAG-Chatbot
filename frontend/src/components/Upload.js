import React, { useState } from "react";
import "./upload.css"; // ✅ Custom CSS file

function Upload() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      setMessage("❗ Please select a file first.");
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setMessage("✅ Upload complete: " + data.filename);
      } else {
        setMessage("❌ Error: " + (data.error || "Upload failed"));
      }
    } catch (err) {
      setMessage("⚠️ Upload error: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-container">
      <h3 className="upload-heading">Upload Your File</h3>
      
      <input
        type="file"
        className="upload-input"
        onChange={(e) => setFile(e.target.files[0])}
      />
      
      <button
        onClick={handleUpload}
        className="upload-button"
        disabled={loading}
      >
        {loading ? "Uploading..." : "Upload"}
      </button>

      {message && <p className="upload-message">{message}</p>}
    </div>
  );
}

export default Upload;
