"""Inject regression evidence from the trusted harness, never from a model claim."""
import copy


def evaluate(module, input_value, context):
    return module.run(
        copy.deepcopy(input_value),
        regression_results=copy.deepcopy(context.get("regression_results")),
        artifact_sha256=context.get("artifact_sha256"),
    )
