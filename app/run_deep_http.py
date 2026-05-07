from runtime.deep_http_analysis import (
    execute_handler,
)

from runtime.memory import RuntimeMemory


appspec = {
    "runtime": {
        "target": "https://example.com",
    }
}

runtime_memory = RuntimeMemory()

result = execute_handler(
    "deep_http_analysis",
    appspec,
    runtime_memory,
)

print(result)

print("\nRuntime Memory:")
print(runtime_memory)
