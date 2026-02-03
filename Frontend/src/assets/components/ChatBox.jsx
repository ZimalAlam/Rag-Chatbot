import { useState } from "react";
import { sendMessage } from "../api/apiClient";

export default function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleSend = async () => {
    if (!input) return;

    const userMsg = { role: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);

    const res = await sendMessage(input);
    const botMsg = { role: "bot", text: res.data.answer };

    setMessages((prev) => [...prev, botMsg]);
    setInput("");
  };

  return (
    <div style={styles.chatContainer}>
      <div style={styles.messages}>
        {messages.map((msg, i) => (
          <div
            key={i}
            style={msg.role === "user" ? styles.userMsg : styles.botMsg}
          >
            {msg.text}
          </div>
        ))}
      </div>
      <div style={styles.inputBox}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask something..."
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
}

const styles = {
  chatContainer: { border: "1px solid #ddd", padding: "10px", height: "400px" },
  messages: { height: "320px", overflowY: "auto" },
  inputBox: { display: "flex", marginTop: "10px" },
  userMsg: { textAlign: "right", margin: "5px", color: "blue" },
  botMsg: { textAlign: "left", margin: "5px", color: "green" },
};
