const express = require("express");
const { Kafka } = require("kafkajs");
const { Pool } = require("pg");

const app = express();
app.use(express.json());

const kafka = new Kafka({ clientId: "sentinel", brokers: ["127.0.0.1:9092"] });
const producer = kafka.producer();
const pool = new Pool({
  user: "admin",
  host: "127.0.0.1",
  database: "sentinel_db",
  password: "password",
  port: 5433,
});

app.post("/api/checkout", async (req, res) => {
  const transaction = req.body;

  try {
    // Force a connection check before sending
    await producer.connect();

    await producer.send({
      topic: "pending-transactions",
      messages: [{ value: JSON.stringify(transaction) }],
    });

    console.log(`✅ Transaction of $${transaction.amount} sent to Kafka`);
    res.status(202).json({ status: "Transaction Sent for Analysis" });
  } catch (error) {
    console.error(" Kafka Producer Error:", error);
    res
      .status(500)
      .json({ error: "Messaging system busy, try again in 2 seconds" });
  }
});

app.get("/api/anomalies", async (req, res) => {
  const result = await pool.query(
    "SELECT * FROM transactions WHERE is_anomaly = TRUE ORDER BY created_at DESC",
  );
  res.json(result.rows);
});

app.listen(5000, () => console.log("Backend running on 5000"));
