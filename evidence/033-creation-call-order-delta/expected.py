"""Exact predicted query tuples derived from the marked-up source bytes."""
import json

CASES = {
    "siblings.ut": (65, 64, "covered"),
    "siblings-all-covered.ut": (68, 67, "covered"),
    "siblings-computed-callee.ut": (69, 68, "unsupported"),
}


def expected():
    rows = {key: [] for key in ("roots", "scopes", "nodes", "edges", "ast_selected")}
    for file, (root_end, second_end, second_status) in CASES.items():
        rows["roots"].append([file, "1", "1", "1", str(root_end), "unsupported", "top-observed", "1"])
        rows["scopes"].extend([
            [file, "1", "10", "1", "34", "covered", "1"],
            [file, "1", "43", "1", str(second_end), second_status, "1"],
        ])

        paths = {
            "top": [
                ("object-identifier", "Identifier:1:4:1:4:MemberExpression:0"),
                ("member-reference", "MemberExpression:1:4:1:6:AssignmentExpression:0"),
                ("function-creation", "FunctionExpression:1:10:1:34:AssignmentExpression:2"),
                ("assignment-completion", "AssignmentExpression:1:4:1:34:ExpressionStatement:0"),
                ("statement-completion", "ExpressionStatement:1:4:1:35:Markup:1"),
                ("object-identifier", "Identifier:1:37:1:37:MemberExpression:0"),
                ("member-reference", "MemberExpression:1:37:1:39:AssignmentExpression:0"),
                ("function-creation", f"FunctionExpression:1:43:1:{second_end}:AssignmentExpression:2"),
                ("assignment-completion", f"AssignmentExpression:1:37:1:{second_end}:ExpressionStatement:0"),
                ("statement-completion", f"ExpressionStatement:1:37:1:{root_end}:Markup:2"),
            ],
            "callable:1:10": [
                ("entry", "entry"),
                ("initializer", "Number:1:31:1:31:VariableDeclarator:2"),
                ("declaration-completion", "LexicalDeclaration:1:23:1:32:StatementBlock:1"),
                ("exit", "exit"),
            ],
        }
        selected = ["VariableDeclarator:1:27:1:31:LexicalDeclaration:1"]
        if file == "siblings.ut":
            paths["callable:1:43"] = [
                ("entry", "entry"),
                ("identifier", "Identifier:1:56:1:59:CallExpression:0"),
                ("call-completion", "CallExpression:1:56:1:61:ExpressionStatement:0"),
                ("statement-completion", "ExpressionStatement:1:56:1:62:StatementBlock:1"),
                ("exit", "exit"),
            ]
            selected.extend(identity for _, identity in paths["callable:1:43"][1:-1])
        elif file == "siblings-all-covered.ut":
            paths["callable:1:43"] = [
                ("entry", "entry"),
                ("initializer", "Number:1:64:1:64:VariableDeclarator:2"),
                ("declaration-completion", "LexicalDeclaration:1:56:1:65:StatementBlock:1"),
                ("exit", "exit"),
            ]
            selected.append("VariableDeclarator:1:60:1:64:LexicalDeclaration:1")
        else:
            selected.extend([
                "SubscriptExpression:1:56:1:63:CallExpression:0",
                "CallExpression:1:56:1:65:ExpressionStatement:0",
                "ExpressionStatement:1:56:1:66:StatementBlock:1",
            ])
        rows["ast_selected"].extend([file, *identity.split(":"), "1"] for identity in selected)
        for scope, path in paths.items():
            rows["nodes"].extend([file, scope, role, identity, "1"] for role, identity in path)
            rows["edges"].extend(
                [file, scope, left, file, scope, right, "1"]
                for (_, left), (_, right) in zip(path, path[1:])
            )
    return rows


if __name__ == "__main__":
    print(json.dumps(expected(), indent=2))
