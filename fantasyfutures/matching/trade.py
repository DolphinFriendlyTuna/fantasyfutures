

class Trade:
    def __init__(self, id, passive_order, aggressive_order, qty):
        self.id = id
        self.passive_order = passive_order
        self.aggressive_order = aggressive_order
        self.qty = qty

    def __repr__(self):
        return f'Trade({self.id}, {self.passive_order}, {self.aggressive_order}, {self.qty})'