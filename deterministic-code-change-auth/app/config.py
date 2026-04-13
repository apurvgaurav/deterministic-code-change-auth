from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Data directories
DATA_DIR = BASE_DIR / "data"
INPUTS_DIR = DATA_DIR / "inputs"
TEMPLATES_DIR = DATA_DIR / "templates"
LEDGER_DIR = DATA_DIR / "ledger"

# Ledger file
LEDGER_FILE = LEDGER_DIR / "authorization_log.jsonl"

# Core system constants
SYSTEM_NAME = "Deterministic Code Change Authorization System"
SYSTEM_VERSION = "0.1.0"

# Replay policy
REPLAY_REQUIRED = True
BYTE_LEVEL_MATCH_REQUIRED = True

# Decision values
DECISION_ALLOW = "ALLOW"
DECISION_BLOCK = "BLOCK"

# Status values
STATUS_SUCCESS = "SUCCESS"
STATUS_FAILURE = "FAILURE"