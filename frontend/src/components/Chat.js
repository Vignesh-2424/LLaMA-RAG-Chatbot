import React, { useState } from "react";
import "./chat.css"; // Custom styling

function Chat() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question.trim()) {
      setError("Please enter a question.");
      return;
    }

    setLoading(true);
    setAnswer("");
    setError(null);

    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || "Something went wrong.");
      } else {
        setAnswer(data.answer);
      }
    } catch (err) {
      setError("Server error: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <h3 className="chat-heading">💬 Ask a Question</h3>
      <div className="chat-input-box">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Type your question..."
          className="chat-input"
        />
        <button onClick={askQuestion} className="chat-button">
          Ask
        </button>
      </div>

      {loading && <div className="chat-loading">⏳ Thinking...</div>}
      {error && <div className="chat-error">{error}</div>}
      {answer && (
        <p className="chat-answer">
          <strong>Answer:</strong> {answer}
        </p>
      )}
    </div>
  );
}

export default Chat;
