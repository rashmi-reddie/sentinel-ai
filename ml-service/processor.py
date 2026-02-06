import json
from kafka import KafkaConsumer
import psycopg2
import time
from model import train_basic_model, predict_fraud

# --- 1. Resilient Connection Helper ---
def get_db_connection():
    return psycopg2.connect(
        host="127.0.0.1", 
        database="sentinel_db", 
        user="admin", 
        password="password", 
        port=5433
    )

# Connect to DB initially
conn = get_db_connection()
cur = conn.cursor()

# Initialize Model
fraud_model = train_basic_model()

# Initialize Kafka
consumer = KafkaConsumer(
    'pending-transactions', 
    bootstrap_servers=['127.0.0.1:9092'],
    api_version=(0, 10, 1),
    auto_offset_reset='earliest',
    group_id='ml-group'
)

print("Sentinel-AI ML Service is active...")

# --- 2. Robust Processing Loop ---
for message in consumer:
    try:
        tx = json.loads(message.value)
        amount = float(tx['amount'])
        
        # Use our model logic
        is_fraud = predict_fraud(fraud_model, amount)
        
        # Check if DB connection is still alive, if not, reconnect
        if conn.closed:
            print("🔄 DB Connection lost. Reconnecting...")
            conn = get_db_connection()
            cur = conn.cursor()

        cur.execute(
            "INSERT INTO transactions (amount, user_id, merchant_id, is_anomaly) VALUES (%s, %s, %s, %s)",
            (amount, tx['user_id'], tx['merchant_id'], bool(is_fraud))
        )
        conn.commit()
        
        status = " FRAUD" if is_fraud else "CLEAR"
        print(f"Processed: ${amount} | Status: {status}")

    except (psycopg2.OperationalError, psycopg2.InterfaceError) as e:
        print(f"DB Error: {e}. Retrying in 2 seconds...")
        time.sleep(2)
        conn = get_db_connection()
        cur = conn.cursor()
    except Exception as e:
        print(f" General Error: {e}")