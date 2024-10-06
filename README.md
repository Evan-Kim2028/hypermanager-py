# hypermanager-py
`hypermanager-py` is an orchestration manager built ontop of the [hypersync python client](https://github.com/enviodev/hypersync-client-python). It is designed to manage block, transaction, and log queries across multiple envio-indexed chains.


### Installation
Install with `pip install hypermanager`. The repository is built with Python 3.12.5. You can easily make a virtual environment for this python version by using [rye](https://rye.astral.sh/guide/installation/) for virtual environment management.

### Example
There is an example that retrieves all log events from the [Across Protocol](https://github.com/across-protocol/contracts) bridging. The example is located in the `examples` directory. Run the example with `python examples/across/spoke_pool_v3.py` to see how to execute a multi-chain events query.
```