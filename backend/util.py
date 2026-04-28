def clean_types(obj):
    import numpy as np
    import math

    if isinstance(obj, dict):
        return {k: clean_types(v) for k, v in obj.items()}

    elif isinstance(obj, list):
        return [clean_types(v) for v in obj]

    elif isinstance(obj, np.integer):
        return int(obj)

    elif isinstance(obj, np.floating):
        val = float(obj)
        if math.isnan(val) or math.isinf(val):
            return None
        return val

    elif isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj

    else:
        return obj