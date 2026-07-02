import os
from cryptography.hazmat.primitives import hashes, hmac


def validate_telegram_init_data(init_data: str) -> dict | None:
    
    try:
        unvalidated_data = sorted(init_data.split('&'))    
    except Exception:
        return None
    
    validated_data = []
    hash = ''
    for data in unvalidated_data:
        if not data.startswith('hash='):
            validated_data.append(data)
        else:
            hash+=str(data).split('=')[1]
            
    h = hmac.HMAC("WebAppData".encode(), hashes.SHA256())
    h.update(os.getenv('TOKEN_TG').encode())
    secret_key = h.finalize()
    
    data_check_string = '\n'.join(validated_data)
    
    try:
        h = hmac.HMAC(secret_key, hashes.SHA256())
        h.update(data_check_string.encode())
        if hash == h.finalize().hex():
            return {item.split('=', 1)[0]: item.split('=', 1)[1] for item in validated_data}
        else:
            return None
    except Exception as e:
        print(e)
        return None
    
    