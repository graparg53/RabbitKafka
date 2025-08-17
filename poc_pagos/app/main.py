from fastapi import FastAPI
from app.models import PaymentRequest
from app.services.payment_service import PaymentValidator
from app.services.queue_service import RabbitMQPublisher

app = FastAPI()

@app.post("/validate-payment")
async def validate_payment(payment: PaymentRequest):
    # Validación síncrona
    validation_result = PaymentValidator.validate(payment.amount)
    
    # Publicación asíncrona solo si es exitoso
    if validation_result["status"] == "success":
        publisher = RabbitMQPublisher()
        publisher.publish(payment.document, payment.amount)
    
    return validation_result