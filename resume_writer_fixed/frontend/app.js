import React, { useState } from "react";
import { createRoot } from "react-dom/client";

function App() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    phone: "",
    template: "template1",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch("http://localhost:5000/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });

    if (!response.ok) {
      alert("Failed to generate resume");
      return;
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "resume.pdf";
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  };

  return (
    <div style={{ maxWidth: 600, margin: "50px auto", fontFamily: "Arial" }}>
      <h1>Resume Generator</h1>
      <form onSubmit={handleSubmit}>
        <input name="name" placeholder="Full Name" onChange={handleChange} required style={{ width: "100%", marginBottom: 10 }} />
        <input name="email" placeholder="Email" onChange={handleChange} required style={{ width: "100%", marginBottom: 10 }} />
        <input name="phone" placeholder="Phone" onChange={handleChange} required style={{ width: "100%", marginBottom: 10 }} />
        <select name="template" onChange={handleChange} style={{ width: "100%", marginBottom: 10 }}>
          <option value="template1">Template 1</option>
        </select>
        <button type="submit">Generate Resume</button>
      </form>
    </div>
  );
}

const root = createRoot(document.getElementById("root"));
root.render(<App />);
