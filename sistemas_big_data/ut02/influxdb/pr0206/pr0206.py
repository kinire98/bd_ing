import os

from extract_data import extract_data
from insert_influx import insert_influx


if __name__ == "__main__":
    base_dir = "./datasets/"
    for dir in os.listdir(path=base_dir):
        data = extract_data(base_dir + dir)
        insert_influx(data)
