# power_distribution.py
"""
A simple model of the typical electricity distribution hierarchy:
Generation -> Transmission -> Substation -> Distribution -> Consumer
"""

class Generation:
    def __init__(self, name):
        self.name = name
    def generate(self):
        print(f"{self.name}: Generating electricity.")
        return 'electricity'

class Transmission:
    def __init__(self, name):
        self.name = name
    def transmit(self, electricity):
        print(f"{self.name}: Transmitting {electricity}.")
        return electricity

class Substation:
    def __init__(self, name):
        self.name = name
    def step_down(self, electricity):
        print(f"{self.name}: Stepping down voltage of {electricity}.")
        return electricity

class Distribution:
    def __init__(self, name):
        self.name = name
    def distribute(self, electricity):
        print(f"{self.name}: Distributing {electricity} to consumers.")
        return electricity

class Consumer:
    def __init__(self, name):
        self.name = name
    def consume(self, electricity):
        print(f"{self.name}: Consuming {electricity}.")

if __name__ == "__main__":
    # Example flow
    gen = Generation("Power Plant")
    trans = Transmission("High Voltage Line")
    sub = Substation("City Substation")
    dist = Distribution("Local Distribution Line")
    cons = Consumer("Residential Area")

    e = gen.generate()
    e = trans.transmit(e)
    e = sub.step_down(e)
    e = dist.distribute(e)
    cons.consume(e) 