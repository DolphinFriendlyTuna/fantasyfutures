import random
from collections import deque
from unittest import TestCase

from fantasyfutures.matching import OrderBook, Order


class OrderBookTests(TestCase):

    def setUp(self):
        random.seed(0)  # force deterministic behaviour.
        self.orderbook = OrderBook(print)

    def test_orderbook_random(self):
        ob = self.orderbook
        for i in range(1, 1000):
            ob.new_order(Order(i,
                               random.choice((Order.Side.BUY, Order.Side.SELL)),
                               random.randrange(1990, 2010),
                               random.randrange(100, 200)))
            print(ob)

        print('finished')
        print(ob)

    def test_orderbook_new_modify_cancel(self):
        ob = self.orderbook
        order = Order(1, Order.Side.BUY, 99.99, 100)
        ob.new_order(order)

        self.assertEqual(0, len(ob.asks))
        self.assertEqual({order.price: deque([order])}, dict(ob.bids))

        new_order = Order(2, Order.Side.BUY, 99.99, 50)
        ob.modify_order(order, new_order)

        self.assertEqual(0, len(ob.asks))
        self.assertEqual({new_order.price: deque([new_order])}, dict(ob.bids))

        ob.cancel_order(new_order)

        self.assertEqual(0, len(ob.asks))
        self.assertEqual(0, len(ob.bids))



