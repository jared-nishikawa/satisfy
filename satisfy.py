import sys

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
        "refinery": 30,
        "blender": 75,
        "particle_accelerator": 1000,
        }


ore = {"iron_ore", "coal", "copper_ore", "limestone", "raw_quartz", "bauxite", "caterium_ore", "sulfur"}
base = {"plastic", "rubber", "water", "nitrogen_gas"}
recipes = {
        "smart_plating": ({"reinforced_plate": 2, "rotor": 2}, 2, "assembler"),
        "reinforced_plate": ({"iron_plate": 30, "screw": 60}, 5, "assembler"),
        "iron_plate": ({"iron_ingot": 30}, 20, "constructor"),
        "iron_ingot": ({"iron_ore": 30}, 30, "smelter"),
        "screw": ({"iron_rod": 10}, 40, "constructor"),
        "iron_rod": ({"iron_ingot": 15}, 15, "constructor"),
        "rotor": ({"iron_rod": 20, "screw": 100}, 4, "assembler"),
        "versatile_framework": ({"modular_frame": 2.5, "steel_beam": 30}, 5, "assembler"),
        "modular_engine": ({"motor": 2, "rubber": 15, "smart_plating": 2}, 1, "manufacturer"),
        "adaptive_control_unit": ({"automated_wiring": 7.5, "circuit_board": 5, "heavy_modular_frame": 1, "computer": 1}, 1, "manufacturer"),
        "automated_wiring": ({"stator": 2.5,  "cable": 50}, 2.5, "assembler"),
        "modular_frame": ({"reinforced_plate": 3, "iron_rod": 12}, 2, "assembler"),
        "steel_beam": ({"steel_ingot": 60}, 15, "constructor"),
        "steel_ingot": ({"iron_ore": 45, "coal": 45}, 45, "foundry"),
        "motor": ({"rotor": 10, "stator": 10}, 5, "assembler"),
        "stator": ({"steel_pipe": 15, "wire": 40}, 5, "assembler"),
        "steel_pipe": ({"steel_ingot": 30}, 20, "constructor"),
        "wire": ({"copper_ingot": 15}, 30, "constructor"),
        "copper_ingot": ({"copper_ore": 30}, 30, "smelter"),
        "cable": ({"wire": 60}, 30, "constructor"),
        "copper_sheet": ({"copper_ingot": 20}, 10, "constructor"),
        "heavy_modular_frame": ({"modular_frame": 10, "steel_pipe": 30, "encased_beam": 10, "screw": 200}, 2, "manufacturer"),
        "encased_beam": ({"steel_beam": 24, "concrete": 30}, 6, "assembler"),
        "concrete": ({"limestone": 45}, 15, "constructor"),
        "computer": ({"circuit_board": 25, "cable": 22.5, "plastic": 45, "screw": 130}, 2.5, "manufacturer"),
        "circuit_board": ({"copper_sheet": 15, "plastic": 30}, 7.5, "assembler"),
        "quartz_crystal": ({"raw_quartz": 37.5}, 22.5, "constructor"),
        "silica": ({"raw_quartz": 22.5}, 37.5, "constructor"),
        "crystal_oscillator": ({"quartz_crystal": 18, "cable": 14, "reinforced_plate": 2.5}, 1, "manufacturer"),

        "caterium_ingot": ({"caterium_ore": 45}, 15, "smelter"),
        "quickwire": ({"caterium_ingot": 12}, 60, "constructor"),
        "ai_limiter": ({"copper_sheet": 25, "quickwire": 100}, 5, "assembler"),
        "electromagnetic_control_rod": ({"stator": 6, "ai_limiter": 4}, 4, "assembler"),

        "sulfuric_acid": ({"sulfur": 50, "water": 50}, 50, "refinery"),
        "battery": ({"sulfuric_acid": 50, "alumina_solution": 40, "aluminum_casing": 20}, 20, "blender"),
        "copper_powder": ({"copper_ingot": 300}, 50, "constructor"),

        "alumina_solution": ({"bauxite": 12, "water": 180}, 120, "refinery"),
        "aluminum_scrap": ({"alumina_solution": 240, "coal": 120}, 360, "refinery"),
        "aluminum_ingot": ({"aluminum_scrap": 90, "silica": 75}, 60, "foundry"),
        "aluminum_casing": ({"aluminum_ingot": 90}, 60, "constructor"),
        "fused_modular_frame": ({"heavy_modular_frame": 1.5, "aluminum_casing": 75, "nitrogen_gas": 37.5}, 1.5, "blender"),
        "radio_control_unit": ({"aluminum_casing": 40, "crystal_oscillator": 1.25, "computer": 1.25}, 2.5, "manufacturer"),
        "pressure_conversion_cube": ({"fused_modular_frame": 1, "radio_control_unit": 2}, 1, "assembler"),

        "high_speed_connector": ({"quickwire": 210, "cable": 37.5, "circuit_board": 3.75}, 3.75, "manufacturer"),
        "supercomputer": ({"computer": 3.75, "ai_limiter": 3.75, "high_speed_connector": 5.625, "plastic": 52.5}, 1.875, "manufacturer"),

        "alclad_aluminum_sheet": ({"aluminum_ingot": 30, "copper_ingot": 10}, 30, "assembler"),
        "heat_sink": ({"alclad_aluminum_sheet": 37.5, "copper_sheet": 22.5}, 7.5, "assembler"),

        "cooling_system": ({"heat_sink": 12, "rubber": 12, "water": 30, "nitrogen_gas": 150}, 6, "blender"),
        "modular_engine": ({"motor": 2, "rubber": 15, "smart_plating": 2}, 1, "manufacturer"),
        "turbo_motor": ({"cooling_system": 7.5, "radio_control_unit": 3.75, "motor": 7.5, "rubber": 45}, 1.875, "manufacturer"),

        "assembly_director_system": ({"adaptive_control_unit": 1.5, "supercomputer": 0.75}, 0.75, "assembler"),
        "magnetic_field_generator": ({"versatile_framework": 2.5, "battery": 5, "electromagnetic_control_rod": 1}, 1, "manufacturer"),
        "nuclear_pasta": ({"copper_powder": 100, "pressure_conversion_cube": 0.5}, 0.5, "particle_accelerator"),
        "thermal_propulsion_rocket": ({"modular_engine": 2.5, "turbo_motor": 1, "cooling_system": 3, "fused_modular_frame": 1}, 1, "manufacturer"),
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
    if not sys.argv[1:]:
        sys.exit(f"{sys.argv[0]} [item] [per/min=1]")
    g = Graph()
    item = sys.argv[1]
    if not sys.argv[2:]:
        rate = recipes[item][1]
    else:
        rate = float(sys.argv[2])

    # initialize graph
    #g.visit("versatile_framework", 16, verbose=True)
    #g.visit("smart_plating", 10, verbose=True)
    #g.visit("motor", 15, verbose=True)
    #g.visit("heavy_modular_frame", 2, verbose=True)
    #g.visit("screw", 500, verbose=True)
    #g.visit("encased_beam", 25, verbose=True)
    #g.visit("steel_pipe", 75, verbose=True)
    #g.visit("modular_frame", 25, verbose=True)
    #g.visit("computer", 2.5, verbose=True)

    g.visit(item, rate, verbose=True)

