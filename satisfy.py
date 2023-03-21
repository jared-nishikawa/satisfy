# all units are x per minute

class UnknownItemError(BaseException):
    pass


raw = {"iron_ore", "coal", "copper_ore"}
recipes = {
        "smart_plating": ({"reinforced_plate": 2, "rotor": 2}, 2),
        "reinforced_plate": ({"iron_plate": 30, "screw": 60}, 5),
        "iron_plate": ({"iron_ingot": 30}, 20),
        "iron_ingot": ({"iron_ore": 30}, 30),
        "screw": ({"iron_rod": 10}, 40),
        "iron_rod": ({"iron_ingot": 15}, 15),
        "rotor": ({"iron_rod": 20, "screw": 100}, 4),
        "versatile_framework": ({"modular_frame": 2.5, "steel_beam": 30}, 5),
        "modular_frame": ({"reinforced_plate": 3, "iron_rod": 12}, 2),
        "steel_beam": ({"steel_ingot": 60}, 15),
        "steel_ingot": ({"iron_ore": 45, "coal": 45}, 45),
        "motor": ({"rotor": 10, "stator": 10}, 5),
        "stator": ({"steel_pipe": 15, "wire": 40}, 5),
        "steel_pipe": ({"steel_ingot": 30}, 20),
        "wire": ({"copper_ingot": 15}, 30),
        "copper_ingot": ({"copper_ore": 30}, 30),
        }

class Node:
    def __init__(self, name, edges, value):
        self.name = name
        self.edges = edges
        self.value = value
class Graph:
    def __init__(self):
        self.raw = raw
        self.nodes = {}
        for name, recipe in recipes.items():
            n = Node(name, recipe[0], recipe[1])
            self.nodes[name] = n

    def visit(self, item, qty, verbose=False):
        print(f"computing costs for {item} at {qty} units/min")
        raw = {}
        intermed = {}
        stack = [(item, qty, 0)]
        while stack:
            name, q, depth = stack.pop()
            if verbose:
                print("    "*depth + f"{name}: {q}")
            if name in self.raw:
                if name not in raw:
                    raw[name] = 0
                raw[name] += q
                continue
            else:
                if name not in intermed:
                    intermed[name] = 0
                intermed[name] += q
            if name not in self.nodes:
                raise UnknownItemError(name)
            node = self.nodes[name]
            rate = node.value
            for ingredient, num in node.edges.items():
                stack.append((ingredient, num*q/rate, depth+1))
        print("total raw products")
        print(raw)
        print("total intermediate products")
        print(intermed)
        print("-"*30)

# enter item and qty(/min) needed
if __name__ == '__main__':
    # initialize graph
    g = Graph()
    g.visit("versatile_framework", 16, verbose=True)
    g.visit("smart_plating", 2, verbose=True)
    g.visit("motor", 5, verbose=True)

