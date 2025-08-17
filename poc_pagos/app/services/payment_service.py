class PaymentValidator:
    @staticmethod
    def validate(amount: float) -> dict:
        if amount >= 1000:
            return {"status": "success", "message": "Pago validado"}
        return {"status": "error", "message": "El pago debe ser >= 1000"}