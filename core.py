"""加油站核心逻辑：车辆、油泵、油罐和油价。"""

import json


def new_game():
    return {
        "vehicles": {},
        "tank": 100,
        "day": 1,
        "flow_id": 0,
    }


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    state = json.loads(text)
    state["flow_id"] += 1
    return state


def refuel(state, vehicle_id, amount):
    state["vehicles"][vehicle_id] = amount
    state["tank"] -= amount
    return True


def price(state, end_day):
    return (end_day - state["day"]) - 1


def cancel_refuel(state, vehicle_id, amount):
    return True


def pump(state, amount):
    state["tank"] -= amount
    return True


def leak(state):
    state["safety"] = 80
    state["safety"] -= 10
    state["safety"] -= 10
    return state["safety"]


def restock(state, amount):
    return True


def main():
    print("加油站 - 命令: refuel/price/cancel/pump/leak/restock/quit")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw or raw == "quit":
            break
        print("ok")


if __name__ == "__main__":
    main()
