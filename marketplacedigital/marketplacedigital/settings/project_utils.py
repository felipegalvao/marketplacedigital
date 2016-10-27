from decimal import Decimal

def calculate_seller_commission(sale_value):
    seller_commission = (sale_value * Decimal(0.85)) - Decimal(0.50)
    return seller_commission
