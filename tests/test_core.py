import unittest

import core


class TestCore(unittest.TestCase):
    def test_01_no_duplicate_refuel(self):
        state = core.new_game()
        self.assertTrue(core.refuel(state, "V1", 10))
        self.assertFalse(core.refuel(state, "V1", 10))

    def test_02_no_refuel_when_empty(self):
        state = core.new_game()
        state["tank"] = 0
        result = core.refuel(state, "V1", 10)
        self.assertFalse(result)

    def test_03_price_exact(self):
        state = core.new_game()
        self.assertEqual(core.price(state, 4), 3)

    def test_04_cancel_refuel_refunds(self):
        state = core.new_game()
        core.refuel(state, "V1", 10)
        core.cancel_refuel(state, "V1", 10)
        self.assertEqual(state["tank"], 100)

    def test_05_no_pump_on_fault(self):
        state = core.new_game()
        state["pump_fault"] = True
        result = core.pump(state, 10)
        self.assertFalse(result)

    def test_06_leak_once(self):
        state = core.new_game()
        core.leak(state)
        self.assertEqual(state["safety"], 90)

    def test_07_no_restock_when_low(self):
        state = core.new_game()
        state["stock"] = 0
        result = core.restock(state, 10)
        self.assertFalse(result)

    def test_08_load_preserves_flow(self):
        state = core.new_game()
        state["flow_id"] = 6
        loaded = core.load_state(core.save_state(state))
        self.assertEqual(loaded["flow_id"], 6)


if __name__ == "__main__":
    unittest.main()
