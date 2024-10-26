# hypermanager-py
`hypermanager-py` is an orchestration manager built ontop of the [hypersync python client](https://github.com/enviodev/hypersync-client-python). It makes cross-chain log queries easy to manage and works with blocks and transactions data as well.


## Installation
Install with `pip install hypermanager`. The repository is built with Python 3.12.5. You can easily make a virtual environment for this python version by using [rye](https://rye.astral.sh/guide/installation/) for virtual environment management.

## Example
There is an example that retrieves all log events from the [Across Protocol](https://github.com/across-protocol/contracts) bridging. The example is located in the `examples` directory. Run the example with `python examples/across/spoke_pool_v3.py` to see how to execute a multi-chain events query.

## Adding Events:
The EventConfig class is a key component of the HyperManager framework, designed to facilitate efficient querying and processing of blockchain events across various protocols. It encapsulates event details, enables dynamic querying, and specifies data mapping. Contributions are welcome to enhance the framework's capabilities and ensure comprehensive data coverage for cross chain events:

```python
@dataclass
class EventConfig:
    name: str
    signature: str
    contract: Optional[str] = None
    column_mapping: Optional[hypersync.ColumnMapping] = None
```

* name: Human-readable event name
* signature: Unique event signature
* contract: (Optional) Associated contract address
* column_mapping: (Optional) Defines transaction and block data processing1

### Add a new event configuration:
1. Understand the event structure (name, signature, contract address, decoded log fields)
2. Create an EventConfig instance
3. Ensure consistency in data types
4. Add the event to the configuration dictionary and submit a pull request (optional)