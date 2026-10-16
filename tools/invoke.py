"""Execute one Python fixture in a fresh process; no model or network calls."""
import importlib.util
import json
import sys

spec = importlib.util.spec_from_file_location("fixture", sys.argv[1])
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
print(json.dumps(module.run(json.loads(sys.argv[2])), sort_keys=True))

