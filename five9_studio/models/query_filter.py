class Filter:
    """A class to represent a filter for a datastore search.

    Attributes:
        column_name (str): The name of the column to filter on.
        operator (str): The operator to use for the filter.
        value (str): The value to filter on.
    """

    def __init__(self, column_name=None):
        self.column_name = column_name
        self.operator = None
        self.value = None

    def column(self, column_name):
        self.column_name = column_name
        return self

    def equals(self, value):
        self.operator = '='
        self.value = value
        return self

    def not_equals(self, value):
        self.operator = '!='
        self.value = value
        return self

    def greater_than(self, value):
        self.operator = '>'
        self.value = value
        return self

    def less_than(self, value):
        self.operator = '<'
        self.value = value
        return self

    def greater_than_or_equal_to(self, value):
        self.operator = '>='
        self.value = value
        return self

    def less_than_or_equal_to(self, value):
        self.operator = '<='
        self.value = value
        return self

    def starts_with(self, value):
        self.operator = '=%'
        self.value = value
        return self

    def ends_with(self, value):
        self.operator = '%='
        self.value = value
        return self

    def contains(self, value):
        self.operator = '%=%'
        self.value = value
        return self

    def not_starts_with(self, value):
        self.operator = '!%'
        self.value = value
        return self

    def not_ends_with(self, value):
        self.operator = '%!'
        self.value = value
        return self

    def not_contains(self, value):
        self.operator = '%!%'
        self.value = value
        return self

    def regex(self, value):
        self.operator = 'REGEXP'
        self.value = value
        return self

    def to_params(self, index):
        base_key = f"filters[{index}]"
        return {
            f"{base_key}[column_name]": self.column_name,
            f"{base_key}[operator]": self.operator,
            f"{base_key}[value]": self.value
        }
