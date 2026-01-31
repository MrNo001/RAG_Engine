from qdrant_client import QdrantClient
from qdrant_client.http import models as qm


def wait_for_qdrant(client: QdrantClient, timeout_s: float = 30.0) -> None:
    deadline = time.time() + timeout_s
    last_err: Exception | None = None
    while time.time() < deadline:
        try:
            client.get_collections()
            return
        except Exception as e: 
            last_err = e
            time.sleep(0.5)
    raise RuntimeError("Qdrant not ready in time") from last_err