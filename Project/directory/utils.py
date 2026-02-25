from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

def safe_decimal(value, places=2):
    if value is None:
        return None
    
    # 1. Clean the string (remove spaces, keep the minus sign!)
    clean_val = str(value).strip()
    
    # 2. Handle Empty Fields
    # If the CSV cell is empty, return None (which becomes NULL in the DB)
    if not clean_val or clean_val.lower() in ['nan', 'none', '-']:
        return None
        
    try:
        # 3. Convert to Decimal
        number = Decimal(clean_val)
        
        # 4. Optional: Force the correct decimal places to avoid rounding errors
        # This ensures -9.68234 becomes -9.68
        exponent = Decimal(10) ** -places
        return number.quantize(exponent, rounding=ROUND_HALF_UP)
        
    except (InvalidOperation, ValueError):
        # If the text is "ABC" or something unparseable, return None
        return None