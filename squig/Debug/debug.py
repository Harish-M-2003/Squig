import os

class WriteDebugger:
    def __init__(self, path="./debug/ast.txt"):
        self.path = path
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

    def dump(self, data):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(str(data))