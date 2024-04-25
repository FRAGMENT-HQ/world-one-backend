import json

def extract_currency_info(json_objs):
    extracted_data = []
    for obj in json_objs:
        currency_info = {
            "currency_code": obj["currency_code"],
            "currency_description": obj["currency_description"]
        }
        extracted_data.append(currency_info)
    return extracted_data