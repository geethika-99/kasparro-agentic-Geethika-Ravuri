import json
from jsonschema import validate

class ValidatorAgent:
    def validate(self, instance, schema_path):
        try:
            schema = json.load(open(schema_path))
            validate(instance, schema)
            return True, ""
        except Exception as e:
            return False, str(e)