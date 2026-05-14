"""Підставляє uid Prometheus замість плейсхолдерів з grafana.com (community dashboards)."""
from __future__ import annotations

import json
from pathlib import Path

DS = {"type": "prometheus", "uid": "prometheus"}
ROOT = Path(__file__).resolve().parent.parent / "grafana" / "dashboards"


def fix_datasource(obj: object) -> None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "datasource" and isinstance(v, str) and v.startswith("${DS_"):
                obj[k] = DS
            else:
                fix_datasource(v)
    elif isinstance(obj, list):
        for item in obj:
            fix_datasource(item)


def main() -> None:
    for name in ("prometheus-3662.json", "postgres-9628.json", "cadvisor-14282.json"):
        path = ROOT / name
        if not path.is_file():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        data.pop("__inputs", None)
        data.pop("__requires", None)
        fix_datasource(data)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
