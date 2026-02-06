import { useEffect, useState } from "react";

function App() {
  const [anomalies, setAnomalies] = useState([]);

  useEffect(() => {
    const fetchAnomalies = () => {
      fetch("/api/anomalies")
        .then((res) => res.json())
        .then((data) => setAnomalies(data));
    };
    const interval = setInterval(fetchAnomalies, 3000); // Poll every 3s
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: "20px", fontFamily: "sans-serif" }}>
      <h1>Sentinel-AI Dashboard</h1>
      <table border="1" width="100%">
        <thead>
          <tr>
            <th>ID</th>
            <th>Amount</th>
            <th>User</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {anomalies.map((tx) => (
            <tr key={tx.id} style={{ backgroundColor: "#ffe6e6" }}>
              <td>{tx.id}</td>
              <td>${tx.amount}</td>
              <td>{tx.user_id}</td>
              <td>🚨 FLAGGED</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
export default App;
