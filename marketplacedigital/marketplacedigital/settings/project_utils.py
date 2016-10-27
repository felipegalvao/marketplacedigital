from decimal import Decimal

def calculate_seller_commission(sale_value):
    seller_commission = (sale_value * Decimal(0.86)) - Decimal(0.40)
    return seller_commission
