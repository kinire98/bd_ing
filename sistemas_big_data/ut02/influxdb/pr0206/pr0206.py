import os

from extract_data import extract_data
from insert_influx import insert_influx

if __name__ == "__main__":
    base_dir = "./datasets/"
    coin_data = []
    for dir in os.listdir(path=base_dir):
        coin_data.append(extract_data(base_dir + dir))
    insert_influx(coin_data)
