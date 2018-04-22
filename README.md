>> Download objects from S3

This small demo project downloads objects from your S3 bucket. You can pass a prefix from a file or a folder and it will download to your `$HOME + $DOWNLOAD_PATH` (it's defined on the `.env` file).

First, rename the `.env.example` file to only `.env` then make the necessary configurations there.

To the script, use:
```python
$ python3 app.py
```

You will see a window where you just paste the prefix and it will download.