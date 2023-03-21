# all units are x per minute

class UnknownItemError(BaseException):
    pass

raw = {"iron_ore", "coal"}
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
        }
        

def add_cost(cost1, cost2):
    c = {}
    for item, value in cost1.items():
        c[item] = value
    for item, value in cost2.items():
        if item not in c:
            c[item] = 0
        c[item] += value
    return c


# enter item and qty(/min) needed
def compute_cost(item, qty):
    cost = {}
    if item not in recipes:
        raise UnknownItemError(item)
    recipe = recipes[item]
    rate = recipe[1]
    for ingredient, num in recipe[0].items():
        if ingredient not in cost:
            cost[ingredient] = 0
        cost[ingredient] += num * (qty/rate)
    return cost


def to_raw(cost):
    raw_cost = {}
    for ingredient, num in cost.items():
        if ingredient not in raw:
            c = compute_cost(ingredient, num)
            r = to_raw(c)
            raw_cost = add_cost(raw_cost, r)
        else:
            raw_cost = add_cost(raw_cost, {ingredient: num})
    return raw_cost

if __name__ == '__main__':
    c = compute_cost("smart_plating", 16)
    print(to_raw(c))
    print(to_raw(compute_cost("versatile_framework", 10)))

