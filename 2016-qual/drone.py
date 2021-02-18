claass Drone(object):

    '''
    Drone 
    '''

    def __init__ (self, row: int, col: int, max_load: int, weights: list):
        self.location = (row, col)
        self.max_load = max_load
        self.current_load = 0
        self.items = {}
        self.destination = (row, col)

        #Ideas?:
        #   Assumption: drone only carries products related to an order
        #   

    def deliver(self, delivery_location: tuple, order: Order):
        if self.location == delivery_location :
            self.items = {}
            self.current_load = 0

        #Ideas: 
        #   Give order to drone, so multiple drones can fulfill the
        #       same order when total weight of items exceeds max_load 