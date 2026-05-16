from llvmlite import ir

class Environment:
    def __init__(self):
        self.records: dict[str, tuple[ir.Value, ir.Type]] = {}

    def set(self, name: str, value: ir.Value, type: ir.Type):
        self.records[name] = (value, type)

    def get(self, name: str):
        return self.records[name]