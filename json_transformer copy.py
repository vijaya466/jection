import json

def sanitize_key(key):
    return key.strip()

def transform_value(value_type, value):
    if value_type == 'S':
        return str(value).strip()
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
        print("tyep is list now...")
        if isinstance(value, list) and value:
            transformed_json = []
            for sub in value:
                if isinstance(sub, dict) and sub:
                    print("sub...", sub)
                    type = list(sub.keys())[0]
                    t_value = list(sub.values())[0]
                    if t_value.strip() and type not in ["NULL", "M", "L"]:
                        print("instde list element proceesing ...")
                        r = transform_value(type,t_value)
                        print("list lement r...",r)
                        if r or type == "BOOL":
                            transformed_json.append(r)
            return transformed_json if len(transformed_json)>0 else None
            return [transform_value(sub['type'], sub['value']) for sub in value if sub['value'].strip()]
        else:
            return None
    elif value_type == 'M':
        if isinstance(value, dict) and value:
            # transformed_map = {}
            # for k, v in sorted(value.items()):
            #     sanitized_key = sanitize_key(k)
            #     transformed_map[sanitized_key] = transform_value(v['type'], v['value'])
            # return transformed_map
            return transform_json(value)
        else:
            return None
    else:
        return None

def transform_json(input_json):
    print("nested again~~~~~~~~~~~~~")
    transformed_json = []
    print("keys......", [key for key, value in input_json.items()])
    for key, value in input_json.items():
        print("key...", key)
        sanitized_key = sanitize_key(key)
        print("sanitized_key...",sanitized_key)
        if sanitized_key:
            print("inside id santizied key ...", value, "\n",list(value.keys()), "\n",list(value.values()) )
            transformed_value = transform_value(list(value.keys())[0], list(value.values())[0])
            print("transfertd value =====",transformed_value)
            if transformed_value is not None:
                transformed_json.append({sanitized_key: transformed_value})
        print("----------------------------------------------")
    return transformed_json

def main():
    # Read input JSON from file
    with open('input.json', 'r') as file:
        input_json = json.load(file)

    transformed_json = transform_json(input_json)
    print(json.dumps(transformed_json, indent=2))

if __name__ == "__main__":
    main()
