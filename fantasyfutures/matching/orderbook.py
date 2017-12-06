from collections import defaultdict, deque

from fantasyfutures.matching.trade import Trade


class OrderBook:
    def __init__(self, *subscribers):
        self.bids = defaultdict(deque)  # TODO, this needs a class.
        self.asks = defaultdict(deque)

        self._trade_id = 1
        self._subscribers = subscribers

    def __repr__(self):
        return 'OrderBook()'

    def __str__(self):
        def agg_level_str(price, orders):
            qty = sum([o.unfilled_qty for o in orders])
            return f'{price}\t{qty}'

        lines = ['OrderBook:']
        lines.append('-----------')
        asks = []
        for price in sorted(self.asks, reverse=True):
            orders = self.asks[price]
            if orders:
                asks.append(agg_level_str(price, orders))

            if len(asks) == 5:
                break

        lines.extend(asks)
        lines.append('-----------')

        bids = []
        for price in sorted(self.bids, reverse=True):
            orders = self.bids[price]
            if orders:
                bids.append(agg_level_str(price, orders))

            if len(bids) == 5:
                break

        lines.extend(bids)
        lines.append('-----------')

        return '\n'.join(lines)

    def add_subscriber(self, subscriber):
        self._subscribers.append(subscriber)

    def remove_subscribers(self, subscriber):
        self._subscribers.remove(subscriber)

    def new_order(self, order):
        """
        
        :param order: 
        :return: 
        """
        trades = None

        if order.is_buy:
            if self.asks and order.price >= min(self.asks):
                trades = self.new_aggressive_order(order)
        else:
            if self.bids and order.price <= min(self.bids):
                trades = self.new_aggressive_order(order)

        if not order.is_filled:
            self.new_passive_order(order)

        # publish the new order in the market data
        self.publish(order)

        # publish the trades
        if trades:
            self.publish(trades)

    def new_passive_order(self, passive):
        levels = self.bids if passive.is_buy else self.asks
        levels[passive.price].append(passive)

    def new_aggressive_order(self, aggressive):
        """
        
        :param aggressive: 
        :return: 
        """
        trades = []

        if aggressive.is_buy:
            for price in sorted(self.asks):
                if aggressive.is_filled:
                    break

                if price > aggressive.price:
                    break

                orders = self.asks[price]
                trades.extend(
                    self._match_aggressive_order(aggressive, orders))

        else:
            for price in sorted(self.bids, reverse=True):
                if price < aggressive.price:
                    break

                orders = self.bids[price]
                trades.extend(
                    self._match_aggressive_order(aggressive, orders))

        return trades

    def _match_aggressive_order(self, aggressive, passive_orders):
        trades = []
        filled_orders = []
        for passive in passive_orders:

            matched_qty = min(passive.unfilled_qty, aggressive.unfilled_qty)

            trades.append(self.new_trade(passive, aggressive, matched_qty))

            # reduce the order qty

            passive.fill(matched_qty)
            aggressive.fill(matched_qty)

            if passive.is_filled:
                filled_orders.append(passive)

            if aggressive.is_filled:
                break

        for order in filled_orders:
            passive_orders.remove(order)

        return trades

    def publish(self, msg):
        """
        
        :param msg: 
        :return: 
        """
        for s in self._subscribers:
            s(msg)

    def cancel_order(self, order):
        """
        
        :param order: 
        :return: 
        """
        levels = self.bids if order.is_buy else self.asks
        level = levels[order.price]
        level.remove(order)
        order.cancel()

        self.publish(order)

    def modify_order(self, old_order, new_order):
        """
        simple cancel and replace.
        
        :param old_order: 
        :param new_order: 
        :return: 
        """
        self.cancel_order(old_order)
        self.new_order(new_order)

    def new_trade(self, passive_order, aggressive_order, qty):
        self._trade_id += 1
        return Trade(self._trade_id, passive_order, aggressive_order, qty)
