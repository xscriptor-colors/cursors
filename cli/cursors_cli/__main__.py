"""Allow ``python -m cursors_cli`` when ``cli/`` is on PYTHONPATH."""

from .cli import main

raise SystemExit(main())
