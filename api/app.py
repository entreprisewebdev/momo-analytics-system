from fastapi import FastAPI
from api.schemas import TransactionResponse

app = FastAPI(
    title="MoMo Analytics System API",
    description="API for Mobile Money transaction analytics",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"message": "MoMo Analytics System API is running"}


@app.get("/transactions/1", response_model=TransactionResponse)
def get_transaction():
    return {
        "transaction_id": 1,
        "amount": 5000.00,
        "transaction_time": "2026-09-10T08:30:00",
        "processed_by": "System",
        "status": "SUCCESS",
        "category": {
            "category_id": 1,
            "category_name": "TRANSFER",
            "description": "Money transferred between users"
        },
        "participants": [
            {
                "user": {
                    "user_id": 1,
                    "phone_number": "0788000001",
                    "name": "Jean Claude"
                },
                "role": "SENDER"
            },
            {
                "user": {
                    "user_id": 2,
                    "phone_number": "0788000002",
                    "name": "Aline Mukamana"
                },
                "role": "RECEIVER"
            }
        ],
        "system_logs": [
            {
                "log_id": 1,
                "transaction_id": 1,
                "log_message": "Transaction processed successfully",
                "log_level": "INFO",
                "log_time": "2026-09-10T08:30:05"
            }
        ]
    }