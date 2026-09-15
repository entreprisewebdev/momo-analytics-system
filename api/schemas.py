from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class UserResponse(BaseModel):
    user_id: int
    phone_number: str
    name: str


class CategoryResponse(BaseModel):
    category_id: int
    category_name: str
    description: Optional[str] = None


class ParticipantResponse(BaseModel):
    user: UserResponse
    role: str


class SystemLogResponse(BaseModel):
    log_id: int
    transaction_id: int
    log_message: str
    log_level: str
    log_time: datetime


class TransactionResponse(BaseModel):
    transaction_id: int
    amount: float
    transaction_time: datetime
    processed_by: str
    status: str
    category: CategoryResponse
    participants: List[ParticipantResponse]
    system_logs: List[SystemLogResponse]