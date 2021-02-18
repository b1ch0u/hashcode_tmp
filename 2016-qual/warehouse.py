class Warehouse(object):

    def __init__(self, row: int, col: int, availability: list, weights: list):
        self.location = (row, col)
        self.availability = availability
        self.weights = weights 

    def load_product_to_drone(self, drone: Drone, product_nb: int, product_quantity: int):
        #This is just a prototype of function
        
        if self.availability[product_nb] >= product_quantity:
            self.availability[product_nb] -= product_quantity
            drone.items[product_nb] += product_quantity


        #Ideas?:
        #   instead of individial products, pass the order
        #   TODO do the weight checking on the warehouse
        pass

    def unload_product_from_drone(self, drone: Drone, product_nb: int, product_quantity: int):
        #This is just a prototype of function
        self.availability[product_nb] += product_quantity
        drone.items[product_nb] -= product_quantity

        #Ideas?:
        #
        pass

