from pydantic import BaseModel

class PaymentRequest(BaseModel):
    document: str
    amount: float