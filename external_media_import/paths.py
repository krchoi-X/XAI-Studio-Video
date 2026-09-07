"""Path safety: reject absolute escapes, .., and symlink escapes."""

from __future__ import annotations

from pathlib import Path, PureWindowsPath


class PathSafetyError(ValueError):
    """Raised when a source path escapes an allowed root."""


def _is_windows_abs(text: str) -> bool:
    p = PureWindowsPath(text)
    return p.is_absolute() or (len(text) >= 2 and text[1] == ":")


def normalize_user_path(raw: str | Path) -> Path:
    return Path(raw).expanduser()


def resolve_without_follow(path: Path) -> Path:
    """Resolve . and .. without requiring the path to exist; do not follow final symlink."""
    return Path(path).absolute()


def ensure_under_allowed_roots(
    candidate: Path,
    allowed_roots: list[Path],
    *,
    label: str = "path",
) -> Path:
    """Return path if it stays under one allowed root.

    Rejects absolute paths outside every allowed root, relative paths that walk
    out via .., and symlink escapes (realpath must stay under an allowed root).
    """
    if not allowed_roots:
        raise PathSafetyError(f"{label}: no allowed source roots configured")

    raw = Path(candidate)
    roots_real: list[Path] = []
    for root in allowed_roots:
        root_abs = Path(root).expanduser().resolve()
        roots_real.append(root_abs)

    candidates_to_try: list[Path] = []
    if raw.is_absolute() or _is_windows_abs(str(raw)):
        candidates_to_try.append(Path(raw))
    else:
        for root in roots_real:
            candidates_to_try.append(root / raw)

    last_err = "not under any allowed root"
    for cand in candidates_to_try:
        try:
            lex = resolve_without_follow(cand)
            if cand.exists() or cand.is_symlink():
                real = cand.resolve(strict=False)
            else:
                real = lex

            for root_real in roots_real:
                try:
                    real.relative_to(root_real)
                    lex.relative_to(root_real)
                    return real if (cand.exists() or cand.is_symlink()) else lex
                except ValueError:
                    continue
            last_err = f"{real} not under allowed roots {[str(r) for r in roots_real]}"
        except OSError as exc:
            last_err = str(exc)

    raise PathSafetyError(f"{label}: path escape rejected ({candidate}): {last_err}")


def safe_dest_name(name: str) -> str:
    """Basename only; reject empty / traversal."""
    if not name or not str(name).strip():
        raise PathSafetyError(f"invalid destination filename: {name!r}")
    normalized = str(name).replace("\\", "/")
    base = Path(normalized).name
    if not base or base in {".", ".."}:
        raise PathSafetyError(f"invalid destination filename: {name!r}")
    if base != normalized.rstrip("/").split("/")[-1]:
        raise PathSafetyError(f"destination must be a basename, got {name!r}")
    return base
