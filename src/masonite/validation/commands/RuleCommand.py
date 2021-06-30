"""New Model Command."""


class RuleCommand:
    """
    Creates a new Rule.

    rule
        {name : Name of the rule}
    """

    scaffold_name = "Rule"
    postfix = ""
    template = "/masonite/validation/snippets/scaffold/rule"
    base_directory = "app/rules/"
