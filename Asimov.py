#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
import os
import sys
import re
import plistlib
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import List, Tuple, Optional

GIT_BIN = "/usr/local/bin/git"

RE_TAG_IN_LOG = re.compile(r"(0\.\d+)-(\w+)-(\w+)\s")

RE_DECR_TAG = re.compile(r"^0\.(\d+)(.+)")

RE_COMMIT_LINE = re.compile(r"^\s{4}(.*)")

RE_FILE_LINE = re.compile(r"[R10MAD](\s+.*\.\w+)")

RE_STATION_IN_PATH = re.compile(r'/(J\w+)/')

RE_DOE_COPY_FROM = re.compile(r"\{BUILD_MODULE}/(_?\w+)/Atlas2/")


def _pick_git_bin() -> str:
    if Path(GIT_BIN).exists():
        return GIT_BIN
    sys_git = shutil_which("git")
    return sys_git if sys_git else "git"

def shutil_which(cmd: str) -> Optional[str]:
    for p in os.environ.get("PATH", "").split(os.pathsep):
        cand = Path(p) / cmd
        if cand.exists() and os.access(cand, os.X_OK):
            return str(cand)
    return None

def run_git(args: List[str], repo_path: Path) -> Tuple[int, str, str]:
    env = os.environ.copy()
    env.pop("GIT_DIR", None)
    env.pop("GIT_WORK_TREE", None)
    git = _pick_git_bin()
    p = subprocess.run([git, *args], cwd=str(repo_path),
                       text=True, capture_output=True, env=env)
    return p.returncode, p.stdout, p.stderr

def ensure_repo_head_tag(repo_path: Path, prior_tag: str) -> None:
    rc, out, err = run_git(["rev-parse", "--is-inside-work-tree"], repo_path)
    if rc != 0 or out.strip() != "true":
        raise RuntimeError(f"[probe] Not a git repo: {repo_path}\n{err}")

    rc, _, err = run_git(["rev-parse", "--verify", "HEAD"], repo_path)
    if rc != 0:
        raise RuntimeError(f"[probe] HEAD invalid (no commits?)\n{err}")

    rc, out, _ = run_git(["rev-parse", "-q", "--verify", f"refs/tags/{prior_tag}"], repo_path)
    if rc != 0 or not out.strip():
        run_git(["fetch", "--tags"], repo_path)
        rc2, out2, err2 = run_git(["rev-parse", "-q", "--verify", f"refs/tags/{prior_tag}"], repo_path)
        if rc2 != 0 or not out2.strip():
            raise RuntimeError(f"[probe] Prior tag not found: {prior_tag}\n{err2}")


def get_repo_path(base: Path, station: str) -> Path:
    return (base / "Station_Tech" / station) if ("873" in station or "775" in station) else (base / station)

def get_build_status(repo_path: Path) -> str:
    target_path = repo_path / "buildtarget.txt"

    with target_path.open("r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f]
    target_flat = " ".join(lines).strip()

    if len(lines) == 2:
        print(f"Current build target: {target_flat} ,in main line")
        return "main"

    print(f"Current build target: {target_flat},not in main line")
    return "DOE"

def handle_tag(current_tag: str, station: str, base: Path) -> str:
    if "0.0" in current_tag:
        repo = base / ("Station_Tech" / Path(station) if ("873" in station or "775" in station)
                       else Path(station))

        proc = subprocess.run(
            ["git", "tag", "--sort=-creatordate"],
            cwd=str(repo),
            text=True,
            capture_output=True,
            check=False
        )
        if proc.returncode != 0:
            raise RuntimeError(f"`git tag --sort=-creatordate` fail：\n{proc.stderr}")

        pat = re.compile(rf"^(0\.\d+)-({re.escape(station)})-([^-]+)$")

        for t in proc.stdout.strip().splitlines():
            if pat.match(t):
                print("Prior tag:", t)
                return t

        raise Exception("Could not get prior tag (no 3-part mainline tag found for this station)")
    else:
        m = re.match(r"^0\.(\d+)(.+)", current_tag)
        if not m:
            raise Exception("Could not parse tag")
        prior_tag = f"0.{int(m.group(1)) - 1}{m.group(2)}"
        print("Prior tag:", prior_tag)
        return prior_tag


def get_commit_lines(prior_tag: str, repo_path: Path) -> List[str]:
    ensure_repo_head_tag(repo_path, prior_tag)
    rc, out, err = run_git(
        ["log", f"{prior_tag}..HEAD", "--name-status", "--no-merges", "-M", "-C"],
        repo_path
    )
    if rc != 0:
        raise RuntimeError(
            "git log failed\n"
            f"repo_path: {repo_path}\n"
            f"cmd: git log {prior_tag}..HEAD --name-status --no-merges -M -C\n"
            f"stderr:\n{err}"
        )
    return out.strip().splitlines()

def check_doe_path(input_target: str, repo_path: Path) -> str:
    m = re.match(r"0\.\d+-(\w+)-(\w+)-(\w+)", input_target)
    only_when = m.group(3) if m else ""
    doe_path = ""

    with (repo_path / "buildconfig.plist").open("rb") as f:
        data = plistlib.load(f)
        for phase in data.get("buildPhases", []):
            cond = phase.get("onlyWhenSubcategoryBelongsTo")
            if cond and cond[0] == only_when:
                m2 = RE_DOE_COPY_FROM.search(phase.get("copyFilesFrom", ""))
                if m2:
                    doe_path = m2.group(1)
                    print("DOE path:", doe_path)

    if not doe_path:
        raise Exception("Could not find DOE path")
    return doe_path


def _infer_base_from_repo(repo_path: Path, station: str) -> Path:
    if ("873" in station) or ("775" in station):
        return repo_path.parent.parent.resolve()
    return repo_path.parent.resolve()

def get_change_list(
    current_tag: str,
    station: str,
    status: str,
    repo_path: Path,
    base: str,
) -> List[str]:

    prior_tag = handle_tag(current_tag, station, base)
    lines = get_commit_lines(prior_tag, repo_path)

    mp: dict[str, List[str]] = defaultdict(list)
    commit_msg = ""
    result: List[str] = []

    for ln in lines:
        m_commit = RE_COMMIT_LINE.search(ln)
        if m_commit:
            content = m_commit.group(1)
            if ("release" not in content) and ("Mink" not in content):
                commit_msg = content
            continue

        m_file = RE_FILE_LINE.search(ln)
        if m_file and commit_msg:
            mp[commit_msg].append(m_file.group(1).strip())

    if status == "main":
        for c, file_changes in mp.items():
            for fc in file_changes:
                if "SharedSequence" in fc:
                        if c not in result:
                            result.append(c)
                        break
                else:
                    m_station = RE_STATION_IN_PATH.search(fc)
                    if m_station and m_station.group(1) == station:
                        if c not in result:
                            result.append(c)
                        break
    else:
        doe_dir = check_doe_path(current_tag, repo_path)
        for c, file_changes in mp.items():
            if any(doe_dir in fc for fc in file_changes):
                result.append(c)

    return result

# --------------- Debug/Entry ---------------

def main(current_tag: str, station_arg: str, base_path: str) -> None:

    global input_target, station, repo_path

    input_target = current_tag.strip()
    station = station_arg.strip()
    base_path = base_path.rstrip("/")
    repo_path = f"{base_path}/{station}"

    if "873" in station or "775" in station:
        repo_path = f"{base_path}/Station_Tech/{station}"

    repo_path = Path(repo_path)

    status = get_build_status(repo_path)
    commit_list = get_change_list(input_target, station, status, repo_path, Path(base_path))

    print("Change list:")
    if len(commit_list) == 0:
        print("- Initial commit")
    else:
        for commit in commit_list:
            print("-", commit)

if __name__ == "__main__":
    DEBUG = True

    if DEBUG:
        debug_tag = "0.0-J873QT1PREBURN-EVT-FANNOISE"
        debug_station = "J873QT1PREBURN"
        debug_base = "/Users/device/MiniStudioSystemTest"
        main(debug_tag, debug_station, debug_base)
    else:
        import sys
        if len(sys.argv) < 3 + 1:
            print("Usage: Asimov.py <current_tag> <station> <base_path>")
            sys.exit(1)
        print("###" + sys.argv[1])
        print("###" + sys.argv[2])
        print("###" + sys.argv[3])
        main(sys.argv[1], sys.argv[2], sys.argv[3])
