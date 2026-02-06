Sentinel-AI: Real-Time Fraud Detection Pipeline
Sentinel-AI is a high-performance, distributed microservices system designed to detect fraudulent financial transactions in real-time. By leveraging an Event-Driven Architecture, the system ensures low latency and high scalability for fintech applications.

System Architecture
The system is composed of four primary layers:

API Gateway (Node.js/Express): Handles incoming checkout requests and produces events to Kafka.

Message Broker (Apache Kafka): Decouples the API from the ML processing logic, ensuring system resilience.

ML Analytics Service (Python): Consumes transaction data and utilizes an Isolation Forest model to flag anomalies.

Persistent Storage (PostgreSQL): Stores processed transactions and their anomaly status for audit and visualization.

Tech Stack
Backend: Node.js, Express, KafkaJS

AI/ML: Python, Scikit-Learn, Pandas

Data: PostgreSQL, Apache Kafka, Zookeeper

DevOps: Docker, Docker Compose
...Getting Started
1️. Prerequisites
Docker Desktop (Ensures all services run in a consistent environment)

Node.js v18+ & Python 3.9+

2️. Infrastructure Deployment
Spin up the containerized database and messaging services:

Bash
docker-compose up -d
Note: Allow approximately 30 seconds for Kafka to complete its internal metadata handshake.

3️. Database Schema Initialization
Initialize the transaction ledger in the PostgreSQL container:

Bash
docker exec -it sentinel-ai-db-1 psql -U admin -d sentinel_db -c "CREATE TABLE transactions (id SERIAL PRIMARY KEY, amount FLOAT, user_id INT, merchant_id INT, is_anomaly BOOLEAN, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"
..Running the Services
ML Processing Service
Bash
cd ml-service
pip install -r requirements.txt
python processor.py
Backend API Gateway
Bash
cd backend
npm install
node index.js
...Testing the Pipeline
Use the following PowerShell command to simulate a high-value checkout attempt ($150,000). The ML service will automatically intercept this event via Kafka and flag it as an anomaly.

PowerShell
powershell -Command "Invoke-RestMethod -Uri http://localhost:5000/api/checkout -Method Post -ContentType 'application/json' -Body '{\"amount\": 150000, \"user_id\": 202, \"merchant_id\": 9}'"
Expected Outcome:

Node.js: Logs Transaction sent to Kafka.

Python: Logs Processed: $150000.0 | Status: FRAUD.

PostgreSQL: New record created with is_anomaly = true.
