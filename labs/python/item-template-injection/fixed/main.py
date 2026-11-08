"""Render an item name through a deliberately small text template engine."""
import ast
import operator
import re

OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul}


def expression(text, context):
    tree = ast.parse(text.strip(), mode="eval")
    if len(list(ast.walk(tree))) > 32:
        raise ValueError("expression too large")
    def visit(node):
        if isinstance(node, ast.Name) and node.id in context:
            return context[node.id]
        if isinstance(node, ast.Constant) and type(node.value) is int and abs(node.value) <= 10000:
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in OPS:
            left, right = visit(node.left), visit(node.right)
            if type(left) is not int or type(right) is not int:
                raise ValueError("integer operands required")
            result = OPS[type(node.op)](left, right)
            if abs(result) > 100000000:
                raise ValueError("result too large")
            return result
        raise ValueError("unsupported expression")
    return str(visit(tree.body))


def render(template, context):
    return re.sub(r"\{\{(.*?)\}\}", lambda match: expression(match[1], context), template)


def run(request):
    name = request.get("name") if isinstance(request, dict) else None
    if not isinstance(name, str) or len(name) > 256 or any(ord(c) < 32 for c in name):
        return {"status": 400, "error": "invalid template"}
    try:
        text = render("Item: {{ name }}", {"name": name})
        return {"status": 200, "text": text}
    except (ValueError, SyntaxError, RecursionError):
        return {"status": 400, "error": "invalid template"}
