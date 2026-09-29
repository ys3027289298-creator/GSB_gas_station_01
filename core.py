"""加油站核心逻辑：车辆、油泵、油罐和油价。"""

import json

TANK_CAPACITY = 100
SAFETY_MAX = 100


def new_game():
    return {
        "vehicles": {},
        "tank": TANK_CAPACITY,
        "stock": TANK_CAPACITY,
        "safety": SAFETY_MAX,
        "pump_fault": False,
        "day": 1,
        "flow_id": 0,
    }


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    state = json.loads(text)
    return state


def refuel(state, vehicle_id, amount):
    if not vehicle_id or amount <= 0:
        return False
    if vehicle_id in state["vehicles"]:
        return False
    if amount > state["tank"]:
        return False
    state["vehicles"][vehicle_id] = amount
    state["tank"] -= amount
    state["flow_id"] += 1
    return True


def price(state, end_day):
    return end_day - state["day"]


def cancel_refuel(state, vehicle_id, amount):
    if vehicle_id not in state["vehicles"]:
        return False
    if state["vehicles"][vehicle_id] != amount:
        return False
    if state["tank"] + amount > TANK_CAPACITY:
        return False
    del state["vehicles"][vehicle_id]
    state["tank"] += amount
    state["flow_id"] += 1
    return True


def pump(state, amount):
    if state.get("pump_fault"):
        return False
    if amount <= 0 or amount > state["tank"]:
        return False
    state["tank"] -= amount
    state["flow_id"] += 1
    return True


def leak(state):
    state["safety"] -= 10
    if state["safety"] < 0:
        state["safety"] = 0
    return state["safety"]


def restock(state, amount):
    if amount <= 0 or amount > state.get("stock", 0):
        return False
    if state["tank"] + amount > TANK_CAPACITY:
        return False
    state["stock"] -= amount
    state["tank"] += amount
    state["flow_id"] += 1
    return True


def main():
    print("加油站 - 命令: refuel/price/cancel/pump/leak/restock/quit")
    state = new_game()
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw:
            continue
        parts = raw.split()
        cmd, args = parts[0], parts[1:]
        if cmd == "quit":
            break
        try:
            if cmd == "refuel" and len(args) == 2:
                print("ok" if refuel(state, args[0], int(args[1])) else "fail")
            elif cmd == "price" and len(args) == 1:
                print(price(state, int(args[0])))
            elif cmd == "cancel" and len(args) == 2:
                print("ok" if cancel_refuel(state, args[0], int(args[1])) else "fail")
            elif cmd == "pump" and len(args) == 1:
                print("ok" if pump(state, int(args[0])) else "fail")
            elif cmd == "leak" and not args:
                print(leak(state))
            elif cmd == "restock" and len(args) == 1:
                print("ok" if restock(state, int(args[0])) else "fail")
            elif cmd == "save" and not args:
                print(save_state(state))
            else:
                print("未知命令或参数错误")
        except ValueError:
            print("参数格式错误")


if __name__ == "__main__":
    main()
