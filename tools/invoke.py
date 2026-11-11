"""Execute a Python fixture, optionally observed by a separate trusted oracle."""
import argparse
import importlib.util
import json
import sys


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source")
    parser.add_argument("input", help="JSON-encoded fixture input")
    parser.add_argument("--oracle", help="Named observer implemented by trusted tooling")
    parser.add_argument("--context", help="JSON-encoded trusted oracle context")
    args = parser.parse_args(argv)
    if args.context is not None and args.oracle is None:
        parser.error("--context requires --oracle")
    input_value = json.loads(args.input)
    context = json.loads(args.context) if args.context is not None else {}
    oracle_fn = None
    if args.oracle:
        # Bind trusted observation function before the candidate's import side effects.
        from repair_oracles import prepare
        oracle_fn = prepare(args.oracle)
        if not isinstance(context, dict):
            parser.error("--context must encode a JSON object")
    spec = importlib.util.spec_from_file_location("fixture", args.source)
    if spec is None or spec.loader is None:
        parser.error("Cannot load fixture source")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    result = oracle_fn(module, input_value, context) if oracle_fn else module.run(input_value)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
