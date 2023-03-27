# all units are x per minute

class UnknownItemError(BaseException):
    pass


machines = {
        "constructor": 4,
        "assembler": 15,
        "manufacturer": 55,
        "foundry": 16,
        "smelter": 4,
        "miner1": 5,
        "miner2": 12,
        }


ore = {"iron_ore", "coal", "copper_ore", "limestone"}
base = {"plastic", "rubber"}
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
        "cable": ({"wire": 60}, 60, "constructor"),
        "copper_sheet": ({"copper_ingot": 20}, 10, "constructor"),
        "heavy_modular_frame": ({"modular_frame": 10, "steel_pipe": 30, "encased_beam": 10, "screw": 200}, 2, "manufacturer"),
        "encased_beam": ({"steel_beam": 24, "concrete": 30}, 6, "assembler"),
        "concrete": ({"limestone": 45}, 15, "constructor"),
        "computer": ({"circuit_board": 25, "cable": 22.5, "plastic": 45, "screw": 130}, 2.5, "manufacturer"),
        "circuit_board": ({"copper_sheet": 15, "plastic": 30}, 7.5, "assembler"),
        }

class Node:
    def __init__(self, name, edges, value, machine):
        self.name = name
        self.edges = edges
        self.value = value
        self.machine = machine

class Graph:
    def __init__(self):
        self.nodes = {}
        for name, recipe in recipes.items():
            n = Node(name, recipe[0], recipe[1], recipe[2])
            self.nodes[name] = n

    def visit(self, item, qty, verbose=False):
        print(f"computing costs for {item} at {qty} units/min")
        total_ore = {}
        intermed = {}
        total_machines = {}
        stack = [(item, qty, 0)]
        while stack:
            name, q, depth = stack.pop()
            if name in ore:
                if verbose:
                    print("    "*depth + f"{name}: {q}")
            elif name in base:
                if verbose:
                    print("    "*depth + f"{name}: {q}")
            else:
                n = self.nodes[name]
                rate = n.value
                machine = n.machine
                if machine not in total_machines:
                    total_machines[machine] = 0
                total_machines[machine] += q/rate
                if verbose:
                    print("    "*depth + f"{name}: {q} ({q/rate} {machine})")
            if name in ore:
                if name not in total_ore:
                    total_ore[name] = 0
                total_ore[name] += q
                continue
            elif name in base:
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
        print("total ore")
        print(total_ore)
        print("total intermediate products")
        print(intermed)
        power = 0
        for mach, num in total_machines.items():
            print(f"{mach}: {num}")
            power += machines[mach] * num
        t_ore = 0
        for _, num in total_ore.items():
            t_ore += num
        ms = []
        for (purity, rate) in (("pure", 240), ("normal", 120), ("impure", 60)):
            num = t_ore/rate
            p = machines["miner2"]
            ms.append(p*num)
            print(f"miners mk2 on {purity} nodes: {num} (power: {p*num})")
        print(f"power: {power+ms[2]} mw (only impure nodes)")
        print(f"power: {power+ms[1]} mw (only normal nodes)")
        print(f"power: {power+ms[0]} mw (only pure nodes)")
        print(f"power: {power} mw (doesn't include miners)")
        print("-"*30)

# enter item and qty(/min) needed
if __name__ == '__main__':
    # initialize graph
    g = Graph()
    #g.visit("versatile_framework", 16, verbose=True)
    #g.visit("smart_plating", 10, verbose=True)
    #g.visit("motor", 15, verbose=True)
    #g.visit("heavy_modular_frame", 5, verbose=True)
    #g.visit("screw", 500, verbose=True)
    #g.visit("encased_beam", 25, verbose=True)
    #g.visit("steel_pipe", 75, verbose=True)
    #g.visit("modular_frame", 25, verbose=True)
    g.visit("computer", 2.5, verbose=True)

