# Causing a timeout error

If you want to timeout a piece of code you have 2 options:

## 1. Signals - Mac/Linux Only

## 2. Async 

```python
import asyncio
async def func_to_timeout():
    # simulate a long-running function
    await asyncio.sleep(5)
    print("Function completed")
try:
    result = await asyncio.wait_for(func_to_timeout(), timeout=6)
    print(result)
except asyncio.TimeoutError:
    print("Function took too long")
```
