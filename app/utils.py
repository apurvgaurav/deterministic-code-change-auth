import hashlib
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_file(file_path: str | Path) -> str:
    path = Path(file_path)
    content = path.read_text(encoding="utf-8")
    return sha256_text(content)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def generate_execution_id() -> str:
    return f"EXEC-{uuid4().hex[:12].upper()}"


def get_environment_fingerprint() -> str:
    raw = "|".join(
        [
            platform.system(),
            platform.release(),
            platform.machine(),
            platform.python_implementation(),
            platform.python_version(),
            sys.executable,
        ]
    )
    return sha256_text(raw)