"""Run an example with the ApifyClient pointed at the local CLI proxy (tests only)."""
import os
import runpy
import sys

import apify_client

PROXY = os.environ.get("EXAMPLES_PROXY_URL", "http://127.0.0.1:8765")
_orig_init = apify_client.ApifyClient.__init__


def _init(self, token=None, **kwargs):
    kwargs["api_url"] = PROXY
    kwargs["api_public_url"] = PROXY
    _orig_init(self, token, **kwargs)


apify_client.ApifyClient.__init__ = _init
sys.argv = sys.argv[1:]
runpy.run_path(sys.argv[0], run_name="__main__")
