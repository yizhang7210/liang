import latency


@latency.require(0)
def hello_world():
    print("Hello world!")


hello_world()
