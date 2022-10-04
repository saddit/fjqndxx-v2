
from datetime import datetime
from hashlib import md5

def get_ts() -> int:
    return int(datetime.now().timestamp() * 1000)

def get_sign(params: list) -> str:
    s = '&'.join(sorted(params, reverse=False))
    return md5(s.encode('utf-8')).hexdigest()


def use_sign(dt) -> tuple[str, str]:
    ts = get_ts()

    params = [f"{k}={dt[k]}" for k in dt]
    params.append(f"timestamp={ts}")
	
    # Should be written to header
    # 'Timestamp' and 'Sign'
    return str(ts), get_sign(params)