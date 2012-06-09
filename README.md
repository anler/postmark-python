# postmark-python

Simple Postmark API client

## Super fast demo

Replace `SENDER`, `RECIPIENT` and `API KEY` with the values that fits you, then just run the script, you'll see the output in the terminal

```python
import sys
import logging

import postmark

logger = logging.getLogger("postmark")
channel = logging.StreamHandler(stream=sys.stdout)
formatter = logging.Formatter("%(message)s")
channel.setFormatter(formatter)
logger.addHandler(channel)

if __name__ == '__main__':
    msg = postmark.Message(sender="SENDER", to="RECIPIENT")
    msg.text = "Hello from python"

    client = postmark.Postmark(api_key="API KEY")
    client.sendmail(msg)
```