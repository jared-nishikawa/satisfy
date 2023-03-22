# all units are x per minute

class UnknownItemError(BaseException):
    pass


raw = {"iron_ore", "coal", "copper_ore", "limestone"}
recipes = {
        "smart_plating": ({"reinforced_plate": 2, "rotor": 2}, 2, "assembler"),
        "reinforced_plate": ({"iron_plate": 30, "screw": 60}, 5, "assembler"),
        "iron_plate": ({"iron_ingot": 30}, 20, "constructor"),
        "iron_ingot": ({"iron_ore": 30}, 30, "smelter"),
        "screw": ({"iron_rod": 10}, 40, "constructor"),
        "iron_rod": ({"iron_ingot": 15}, 15, "constructor"),
        "rotor": ({"iron_rod": 20, "screw": 100}, 4, "assembler"),
        "versatile_framework": ({"modular_frame": 2.5, "steel_beam": 30}, 5, "assembler"),
        "modular_frame": ({"reinforced_plate": 3, "iron_rod": 12}, 2, "assembler"),
        "steel_beam": ({"steel_ingot": 60}, 15, "constructor"),
        "steel_ingot": ({"iron_ore": 45, "coal": 45}, 45, "foundry"),
        "motor": ({"rotor": 10, "stator": 10}, 5, "assembler"),
        "stator": ({"steel_pipe": 15, "wire": 40}, 5, "assembler"),
        "steel_pipe": ({"steel_ingot": 30}, 20, "constructor"),
        "wire": ({"copper_ingot": 15}, 30, "constructor"),
        "copper_ingot": ({"copper_ore": 30}, 30, "smelter"),
        "copper_sheet": ({"copper_ingot": 20}, 10, "constructor"),
        "heavy_modular_frame": ({"modular_frame": 10, "steel_pipe": 30, "encased_beam": 10, "screw": 200}, 2, "manufacturer"),
        "encased_beam": ({"steel_beam": 24, "concrete": 30}, 6, "assembler"),
        "concrete": ({"limestone": 45}, 15, "constructor"),
        }

class Node:
    def __init__(self, name, edges, value, machine):
        self.name = name
        self.edges = edges
        self.value = value
        self.machine = machine

class Graph:
    def __init__(self):
        self.raw = raw
        self.nodes = {}
        for name, recipe in recipes.items():
            n = Node(name, recipe[0], recipe[1], recipe[2])
            self.nodes[name] = n

    def visit(self, item, qty, verbose=False):
        print(f"computing costs for {item} at {qty} units/min")
        total_raw = {}
        intermed = {}
        constructors = 0
        assemblers = 0
        foundries = 0
        stack = [(item, qty, 0)]
        while stack:
            name, q, depth = stack.pop()
            if name in self.raw:
                if verbose:
                    print("    "*depth + f"{name}: {q}")
            else:
                n = self.nodes[name]
                rate = n.value
                machine = n.machine
                if machine == "constructor":
                    constructors += q/rate
                elif machine == "assembler":
                    assemblers += q/rate
                elif machine == "foundry":
                    foundries += q/rate
                if verbose:
                    print("    "*depth + f"{name}: {q} ({q/rate} {machine})")
            if name in self.raw:
                if name not in total_raw:
                    total_raw[name] = 0
                total_raw[name] += q
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
        print(total_raw)
        print("total intermediate products")
        print(intermed)
        print("constructors:", constructors)
        print("assemblers:", assemblers)
        print("foundries:", foundries)
        print("-"*30)

# enter item and qty(/min) needed
if __name__ == '__main__':
    # initialize graph
    g = Graph()
    #g.visit("versatile_framework", 16, verbose=True)
    #g.visit("smart_plating", 10, verbose=True)
    #g.visit("motor", 15, verbose=True)
    g.visit("heavy_modular_frame", 5, verbose=True)

