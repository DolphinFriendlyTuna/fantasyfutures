

class Order:
    class Side:
        BUY = 'BUY'
        SELL = 'SELL'

    class State:
        NEW = 'NEW'
        LIVE = 'ACTIVE'
        FILLED = 'FILLED'
        CANCELLED = 'CANCELLED'

    def __init__(self, id, side, price, qty):
        assert side in (Order.Side.BUY, Order.Side.SELL), f'Invalid side {side}'

        self.id = id
        self.side = side
        self.price = price
        self.qty = qty

        self.state = Order.State.NEW
        self.filled_qty = 0

    def __repr__(self):
        return f'Order({self.id}, {self.side}, {self.price}, {self.qty})'

    def __str__(self):
        return f'Order({self.id}, {self.side}, {self.price}, {self.qty})(filled={self.filled_qty})'

    @property
    def is_buy(self):
        return self.side == Order.Side.BUY

    @property
    def unfilled_qty(self):
        return self.qty - self.filled_qty

    @property
    def is_filled(self):
        return self.state == Order.State.FILLED

    @property
    def is_cancelled(self):
        return self.state == Order.State.CANCELLED

    @property
    def is_live(self):
        return self.state == Order.State.LIVE

    def fill(self, qty):
        assert qty <= self.unfilled_qty, f'qty: {qty} too large for {self}.'
        self.filled_qty += qty

        if self.unfilled_qty == 0:
            self.state = Order.State.FILLED

    def activate(self):
        self.state = Order.State.LIVE

    def cancel(self):
        self.state = Order.State.CANCELLED
