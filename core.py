"""加油站核心逻辑：车辆、油泵、油罐和油价。"""

import json

TANK_CAPACITY = 100


def new_game():
    return {
        "vehicles": {},
        "tank": TANK_CAPACITY,
        "day": 1,
        "flow_id": 0,
        "safety": 100,
        "stock": 50,
        "pump_fault": False,
    }


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    state = json.loads(text)
    if not isinstance(state, dict) or "tank" not in state:
        raise ValueError("非法存档数据")
    return state


def _valid_amount(amount):
    return isinstance(amount, (int, float)) and not isinstance(amount, bool) and amount > 0


def refuel(state, vehicle_id, amount):
    if not vehicle_id or not _valid_amount(amount):
        return False
    if vehicle_id in state["vehicles"]:
        return False
    if state["tank"] < amount:
        return False
    state["vehicles"][vehicle_id] = amount
    state["tank"] -= amount
    state["flow_id"] += 1
    return True


def price(state, end_day):
    return end_day - state["day"]


def cancel_refuel(state, vehicle_id, amount):
    if not vehicle_id or not _valid_amount(amount):
        return False
    if state["vehicles"].get(vehicle_id) != amount:
        return False
    del state["vehicles"][vehicle_id]
    state["tank"] = min(TANK_CAPACITY, state["tank"] + amount)
    state["flow_id"] += 1
    return True


def pump(state, amount):
    if state.get("pump_fault"):
        return False
    if not _valid_amount(amount):
        return False
    if state["tank"] < amount:
        return False
    state["tank"] -= amount
    state["flow_id"] += 1
    return True


def leak(state):
    state["safety"] -= 10
    state["flow_id"] += 1
    return state["safety"]


def restock(state, amount):
    if not _valid_amount(amount):
        return False
    if state.get("stock", 0) < amount:
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
        if not raw or raw == "quit":
            break
        parts = raw.split()
        cmd, args = parts[0], parts[1:]
        try:
            if cmd == "refuel" and len(args) == 2:
                ok = refuel(state, args[0], float(args[1]))
            elif cmd == "price" and len(args) == 1:
                print(price(state, int(args[0])))
                continue
            elif cmd == "cancel" and len(args) == 2:
                ok = cancel_refuel(state, args[0], float(args[1]))
            elif cmd == "pump" and len(args) == 1:
                ok = pump(state, float(args[0]))
            elif cmd == "leak" and not args:
                print(leak(state))
                continue
            elif cmd == "restock" and len(args) == 1:
                ok = restock(state, float(args[0]))
            elif cmd == "save" and not args:
                print(save_state(state))
                continue
            else:
                print("非法命令")
                continue
        except ValueError:
            print("非法参数")
            continue
        print("ok" if ok else "失败")


if __name__ == "__main__":
    main()
