import Statistic
import Display
import numpy as np
import pandas as pa

def main():
    best_agents = Statistic.get_best_agents("Dataset/valo_agents_stat")
    Display.RunApp(best_agents)

main()