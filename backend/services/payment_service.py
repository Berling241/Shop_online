import asyncio
import random
from typing import Dict, Any
from models.order import PaymentMethod

class PaymentService:
    """
    Service de simulation des paiements mobiles pour Moov Money et Airtel Money
    Dans un vrai projet, ceci intégrerait les APIs réelles des opérateurs
    """
    
    @staticmethod
    async def process_mobile_payment(
        phone_number: str,
        amount: float,
        payment_method: PaymentMethod,
        order_number: str
    ) -> Dict[str, Any]:
        """
        Simule le traitement d'un paiement mobile
        """
        # Simulation d'un délai de traitement
        await asyncio.sleep(2)
        
        # Validation basique du numéro
        if not phone_number or len(phone_number.replace(' ', '')) < 8:
            return {
                "success": False,
                "error": "Numéro de téléphone invalide",
                "transaction_id": None
            }
        
        # Validation du montant
        if amount <= 0:
            return {
                "success": False,
                "error": "Montant invalide",
                "transaction_id": None
            }
        
        # Simulation de succès/échec (90% de succès)
        success_rate = 0.9
        is_successful = random.random() < success_rate
        
        if is_successful:
            # Génération d'un ID de transaction simulé
            transaction_id = f"TXN{random.randint(100000, 999999)}"
            
            return {
                "success": True,
                "error": None,
                "transaction_id": transaction_id,
                "payment_method": payment_method,
                "amount": amount,
                "phone_number": phone_number,
                "order_number": order_number,
                "message": f"Paiement de {amount:,.0f} FCFA effectué avec succès via {payment_method.upper()}"
            }
        else:
            # Simulation d'erreurs possibles
            errors = [
                "Solde insuffisant",
                "Numéro non reconnu par l'opérateur",
                "Service temporairement indisponible",
                "Transaction annulée par l'utilisateur"
            ]
            
            return {
                "success": False,
                "error": random.choice(errors),
                "transaction_id": None
            }
    
    @staticmethod
    def validate_phone_number(phone_number: str, payment_method: PaymentMethod) -> bool:
        """
        Valide le format du numéro selon l'opérateur
        """
        # Nettoyage du numéro
        clean_number = phone_number.replace(' ', '').replace('-', '').replace('+225', '')
        
        if payment_method == PaymentMethod.MOOV_MONEY:
            # Moov Money : commence généralement par 01, 02, 05
            return len(clean_number) >= 8 and clean_number[:2] in ['01', '02', '05']
        
        elif payment_method == PaymentMethod.AIRTEL_MONEY:
            # Airtel Money : commence généralement par 07, 09
            return len(clean_number) >= 8 and clean_number[:2] in ['07', '09']
        
        return len(clean_number) >= 8  # Validation générique