#!/usr/bin/env python3
"""Refresh and print PROJECT-MAP.md: a compact map of a project folder.

Run from the project's top folder:

    python3 make_project_map.py [--root DIR] [--log NOTES.md] [--entry index.html] [--quiet]

It keeps everything above the AUTO marker in PROJECT-MAP.md (the standing
notes, edited by hand) and rewrites everything below it from the files on disk.
It reads only file names, sizes and dates (plus the entry page and the headings
of the log file, when they exist), so it is fast and changes nothing else.
Standard library only; works on Python 3.8+.
"""
import argparse, os, re, shutil, sys, time
from collections import Counter

MAP_NAME = "PROJECT-MAP.md"
MARK = "<!-- AUTO SNAPSHOT BELOW. Rewritten by make_project_map.py. Do not edit by hand. -->"
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build",
             ".next", ".cache", ".idea", ".vscode", "target"}
MAX_FILES = 200000  # stop walking very large trees


def size(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return ("%d %s" % (n, unit)) if unit == "B" else ("%.1f %s" % (n, unit))
        n /= 1024.0


def day(t):
    return time.strftime("%b %d", time.localtime(t))


def walk(root):
    """Return [(relative path, size, mtime)] for every file, skipping noise folders."""
    out = []
    for base, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith("."))
        for name in files:
            if name.startswith("."):
                continue
            full = os.path.join(base, name)
            try:
                st = os.stat(full, follow_symlinks=False)
            except OSError:
                continue
            out.append((os.path.relpath(full, root), st.st_size, st.st_mtime))
            if len(out) >= MAX_FILES:
                return out, True
    return out, False


def entry_page(root, entry, add):
    path = os.path.join(root, entry)
    if not os.path.exists(path):
        return
    try:
        html = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return
    srcs = re.findall(r'<script[^>]*\ssrc="([^"]+)"', html)
    css = re.findall(r'<link[^>]*rel="stylesheet"[^>]*href="([^"]+)"', html)
    here = os.path.dirname(path)
    missing = [s for s in srcs + css if not s.startswith(("http:", "https:", "//", "data:"))
               and not os.path.exists(os.path.join(here, s.split("?")[0].split("#")[0].lstrip("/")))]
    add("- `%s`: %s, %d script tags, %d stylesheets, %d pointing at a missing file%s" % (
        entry, size(len(html.encode("utf-8"))), len(srcs), len(css), len(missing),
        (" (" + ", ".join(missing[:5]) + ")") if missing else ""))


def log_index(root, log, add):
    path = os.path.join(root, log)
    try:
        lines = open(path, encoding="utf-8", errors="replace").read().split("\n")
    except OSError:
        return
    heads = [(i + 1, l[3:].strip()) for i, l in enumerate(lines) if l.startswith("## ")]
    add("### Index of %s (%s, %d lines)" % (log, size(os.path.getsize(path)), len(lines)))
    add("")
    add("Read one section, never the whole file: `sed -n 'START,ENDp' \"%s\"`. "
        "Each entry is `start line: heading`; a section ends where the next begins." % log)
    add("")
    for n, h in heads:
        add("- %d: %s" % (n, h[:110]))
    add("")


def snapshot(root, entry, log):
    L = []
    add = L.append
    files, capped = walk(root)
    files = [f for f in files if f[0] != MAP_NAME]
    add("## Snapshot (generated %s)" % time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()))
    add("")
    try:
        free = shutil.disk_usage(root).free
        add("- Free disk space: %s%s" % (size(free), "  **LOW: do not create large copies**" if free < 5 * 1024 ** 3 else ""))
    except OSError:
        pass
    add("- Files: %d, %s in total%s" % (len(files), size(sum(f[1] for f in files)),
                                         " (stopped at the file limit; the tree is larger)" if capped else ""))
    ext = Counter((os.path.splitext(f[0])[1].lstrip(".").lower() or "(none)") for f in files)
    add("- By type: " + ", ".join("%d %s" % (c, e) for e, c in ext.most_common(10)))
    tests = sum(1 for f in files if re.search(r"(^|[\\/])(test_[^\\/]*\.py|[^\\/]*[._]test\.[cm]?[jt]sx?|[^\\/]*_test\.(py|go))$", f[0]))
    if tests:
        add("- Test files: %d" % tests)
    entry_page(root, entry, add)
    add("")

    add("### Top-level folders (files inside, total size)")
    add("")
    per, sz = Counter(), Counter()
    for rel, s, _ in files:
        top = rel.split(os.sep)[0] if os.sep in rel else "(top level)"
        per[top] += 1
        sz[top] += s
    add(", ".join("`%s` %d files %s" % (k, c, size(sz[k])) for k, c in per.most_common(25)))
    add("")

    add("### File families (first word of the file name: count)")
    add("")
    fam = Counter(re.split(r"[-._ ]", os.path.basename(f[0]))[0].lower() for f in files)
    add(", ".join("%s %d" % (k, c) for k, c in fam.most_common(30) if c > 1) or "(no repeated prefixes)")
    add("")

    add("### Largest files (never print these whole; search them or load them with a script)")
    add("")
    add(", ".join("`%s` %s" % (f[0], size(f[1])) for f in sorted(files, key=lambda f: -f[1])[:14]))
    add("")

    add("### Changed most recently")
    add("")
    recent = sorted((f for f in files if not f[0].endswith(".log")), key=lambda f: -f[2])[:18]
    add(", ".join("`%s` (%s)" % (f[0], day(f[2])) for f in recent))
    add("")

    if log:
        log_index(root, log, add)
    return "\n".join(L).rstrip() + "\n"


def main():
    ap = argparse.ArgumentParser(description="Refresh and print PROJECT-MAP.md")
    ap.add_argument("--root", default=".", help="project folder (default: current folder)")
    ap.add_argument("--entry", default="index.html", help="entry page to check for missing scripts and stylesheets")
    ap.add_argument("--log", default="", help="a long notes or change-log file whose '## ' headings should be indexed")
    ap.add_argument("--quiet", action="store_true", help="write the map without printing it")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    path = os.path.join(root, MAP_NAME)
    notes = ""
    if os.path.exists(path):
        notes = open(path, encoding="utf-8").read().split(MARK)[0].rstrip()
    if not notes:
        notes = "# Project map: %s\n\n## Standing notes\n\n(none yet)" % os.path.basename(root)
    out = notes + "\n\n" + MARK + "\n\n" + snapshot(root, a.entry, a.log)
    with open(path, "w", encoding="utf-8") as f:
        f.write(out)
    if not a.quiet:
        sys.stdout.write(out)


if __name__ == "__main__":
    main()
