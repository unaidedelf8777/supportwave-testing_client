import os
import json
import re

def delete_file(filepath: str):
    os.remove(filepath)


def validate_json(json_string):
    try:
        parsed_json = json.loads(json_string)
        return parsed_json['message_to_customer'], True
    except ValueError:
        # Pattern to match "message_to_customer":"any value here"
        pattern = r'"message_to_customer"\s*:\s*"([^"]*)"'
        match = re.search(pattern, json_string)
        if match:
            # The value will be in the first group of the match
            return match.group(1), False
        else:
            return None, False


