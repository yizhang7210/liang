from liang import latency
import time
import logging

logging.basicConfig(level=logging.INFO)


@latency.require(1)
def hello_world_require():
    time.sleep(3)
    print("hello world!")


@latency.recommend(1)
def hello_world_recommend():
    time.sleep(3)
    print("hello world!")


def main():
    hello_world_recommend()
    hello_world_require()


if __name__ == '__main__':
    main()
