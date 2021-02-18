class Order(object):

    '''
    Order class will accessed by Drone and Warehouse
    '''

    def __init__ (self, order_nb: int, row: int, col: int, items: dict):
        
        self.order_nb = order_nb
        self.destination = (row, col)
        self.items = items
        self.order_states = ['standby', 'in_process', 'delivered']
        self.state = self.order_states[0]


    def deliver_items (self, product_nb: int):
        self.items[product_nb] = 0

    def check_state (self):
        items_left = 0

        for k in self.items.keys():
            items_left += self.items[k]
        
        if items_left == 0:
            self.state = self.order_states[2]
