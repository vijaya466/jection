import json

def sanitize_key(key):
    return key.strip()

def transform_value(value_type, value):
    if value_type == 'S':
        return str(value.strip())
    elif value_type == 'N':
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return None
    elif value_type == 'BOOL':
        value = str(value).strip().lower()
        if value in ['1', 't', 'true']:
            return True
        elif value in ['0', 'f', 'false']:
            return False
        else:
            return None
    elif value_type == 'NULL':
        value = str(value).strip().lower()
        if value in ['1', 't', 'true']:
            return None
        elif value in ['0', 'f', 'false']:
            return None
        else:
            return None
    elif value_type == 'L':
        if isinstance(value, list) and value:
            transformed_json = []
            for sub in value:
                if isinstance(sub, dict) and sub:
                    type = list(sub.keys())[0]
                    t_value = list(sub.values())[0]
                    if t_value.strip() and type not in ["NULL", "M", "L"]:
                        r = transform_value(type,t_value)
                        if r or type == "BOOL":
                            transformed_json.append(r)
            return transformed_json if len(transformed_json)>0 else None
        else:
            return None
    elif value_type == 'M':
        if isinstance(value, dict) and value:
            return transform_json(value)
        else:
            return None
    else:
        return None

def transform_json(input_json):
    transformed_json = []
    for key, value in input_json.items():
        sanitized_key = sanitize_key(key)
        if sanitized_key:
            transformed_value = transform_value(list(value.keys())[0], list(value.values())[0])
            if transformed_value is not None:
                transformed_json.append({sanitized_key: transformed_value})
    return transformed_json

def main():
    # Read input JSON from file
    with open('input.json', 'r') as file:
        input_json = json.load(file)

    transformed_json = transform_json(input_json)
    print(json.dumps(transformed_json, indent=2))

if __name__ == "__main__":
    main()
