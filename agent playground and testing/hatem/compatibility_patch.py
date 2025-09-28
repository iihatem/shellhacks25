"""Compatibility patch for google-adk==1.9.0 with a2a-sdk==0.3.0."""

import sys
from a2a.client import client as real_client_module
from a2a.client.card_resolver import A2ACardResolver

class PatchedClientModule:
    """Patched client module to fix A2ACardResolver import issue."""
    
    def __init__(self, real_module) -> None:
        for attr in dir(real_module):
            if not attr.startswith('_'):
                setattr(self, attr, getattr(real_module, attr))
        self.A2ACardResolver = A2ACardResolver

def apply_compatibility_patch():
    """Apply the compatibility patch for ADK and A2A SDK."""
    patched_module = PatchedClientModule(real_client_module)
    sys.modules['a2a.client.client'] = patched_module
