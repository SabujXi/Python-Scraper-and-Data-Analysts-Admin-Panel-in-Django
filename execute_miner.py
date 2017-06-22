import miner
from miner import scrape, cities, session
if __name__ == '__main__':
    scrape(cities, session)

else:
    print("Not running as main script")