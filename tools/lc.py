#!/usr/bin/env python3
"""
Simplest local runner for LeetCode-style Python solutions.

Usage:
  # Run by problem id; uses tests/<id>.txt
  python tools/lc.py 0001

  # Or run by explicit path and tests
  python tools/lc.py problems/easy/0001-two-sum.py -t tests/0001.txt

Test file format (paste into tests/<id>.txt):
  nums = [2,7,11,15]
  target = 9
  expected = [0,1]      # optional; asserts when present

Multiple cases: separate them with a blank line.

Extras:
- Automatically converts Python lists to ListNode chains when your solution file
  defines a `ListNode` class and the arg looks like a linked list (e.g. l1, l2, head).
  Expected outputs can be plain lists for linked-list results.
"""

from __future__ import annotations

import argparse
import ast
import glob
import importlib.util
import inspect
import io
import os
from typing import Any, Dict, List, Tuple


def is_problem_id(s: str) -> bool:
    return s.isdigit()


def find_solution_by_id(pid: str) -> str:
    pid4 = pid.zfill(4)
    matches = sorted(glob.glob(os.path.join("problems", "**", f"{pid4}-*.py"), recursive=True))
    if not matches:
        raise FileNotFoundError(f"No Python solution found for id {pid4} under problems/**")
    return matches[0]


def default_tests_path(pid: str) -> str:
    return os.path.join("tests", f"{pid.zfill(4)}.txt")


def load_solution(path: str):
    spec = importlib.util.spec_from_file_location("lc_solution", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import solution from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "Solution"):
        raise AttributeError("Solution class not found in solution file")
    return module.Solution(), module


def choose_method(sol, forced: str | None) -> str:
    if forced:
        if not hasattr(sol, forced):
            raise AttributeError(f"Solution has no method '{forced}'")
        return forced
    methods = [
        name
        for name, func in inspect.getmembers(type(sol), predicate=inspect.isfunction)
        if not name.startswith("_")
    ]
    if len(methods) == 1:
        return methods[0]
    raise SystemExit(
        "Multiple public methods found on Solution. Use --method to choose: "
        + ", ".join(methods)
    )


def split_testcases(content: str) -> List[str]:
    blocks: List[str] = []
    buff: List[str] = []
    for line in content.splitlines():
        if line.strip() == "":
            if buff:
                blocks.append("\n".join(buff))
                buff = []
        else:
            buff.append(line)
    if buff:
        blocks.append("\n".join(buff))
    return blocks


def parse_assignment_block(block: str) -> Tuple[Dict[str, Any], Any]:
    env: Dict[str, Any] = {}
    expected = None
    for raw in block.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            key = f"__arg{len([k for k in env.keys() if k.startswith('__arg')])}__"
            value_src = line
        else:
            key, value_src = line.split("=", 1)
            key = key.strip()
            value_src = value_src.strip()
        try:
            value = ast.literal_eval(value_src)
        except Exception as e:
            raise ValueError(f"Failed to parse value for '{key}': {value_src}\n{e}")
        if key.lower() in {"expected", "output", "result"}:
            expected = value
        else:
            env[key] = value
    return env, expected


def build_args(env: Dict[str, Any], method, module) -> List[Any]:
    sig = inspect.signature(method)
    params = [p for p in sig.parameters.values() if p.name != "self"]
    listnode_cls = getattr(module, "ListNode", None)

    def to_listnode(val):
        if listnode_cls is None:
            return val
        if isinstance(val, list):
            dummy = listnode_cls(0)
            cur = dummy
            for x in val:
                cur.next = listnode_cls(x)
                cur = cur.next
            return dummy.next
        return val

    positional_keys = sorted([k for k in env.keys() if k.startswith("__arg")])
    if positional_keys:
        if len(positional_keys) != len(params):
            raise ValueError(
                f"Positional args provided ({len(positional_keys)}) do not match method arity ({len(params)})."
            )
        return [to_listnode(env[k]) for k in positional_keys]

    args: List[Any] = []
    for p in params:
        if p.name not in env:
            raise KeyError(f"Missing required argument '{p.name}' in testcase block")
        val = env[p.name]
        # Heuristic conversion for linked lists when a ListNode class exists
        if listnode_cls is not None and isinstance(val, list):
            if p.annotation is not inspect._empty:
                ann = p.annotation
                ann_name = getattr(ann, "__name__", str(ann))
                if "ListNode" in ann_name:
                    val = to_listnode(val)
            else:
                if p.name.startswith("l") or p.name.startswith("head"):
                    val = to_listnode(val)
        args.append(val)
    return args


def run_case(sol, method_name: str, env: Dict[str, Any], expected, module):
    method = getattr(sol, method_name)
    args = build_args(env, method, module)
    out = method(*args)

    listnode_cls = getattr(module, "ListNode", None)
    def listnode_to_list(node):
        res = []
        cur = node
        while cur is not None:
            res.append(cur.val)
            cur = cur.next
        return res

    shown_out = out
    if listnode_cls is not None and hasattr(out, "next") and hasattr(out, "val"):
        shown_out = listnode_to_list(out)

    ok = True
    msg = ""
    if expected is not None:
        if shown_out is out:
            ok = out == expected
        else:
            ok = shown_out == expected
        if not ok:
            msg = f"Expected {expected}, got {shown_out}"
    return shown_out, ok, msg


def main():
    ap = argparse.ArgumentParser(description="Run LeetCode-style Python Solution locally (easy mode)")
    ap.add_argument("problem", help="Problem id (e.g., 1 or 0001) or path to solution .py")
    ap.add_argument("-t", "--tests", help="Path to testcase file (defaults to tests/<id>.txt when id is used)")
    ap.add_argument("-m", "--method", help="Method name on Solution to invoke")
    args = ap.parse_args()

    pid = None
    if os.path.exists(args.problem) and args.problem.endswith(".py"):
        solution_path = args.problem
    elif is_problem_id(args.problem):
        pid = args.problem.zfill(4)
        solution_path = find_solution_by_id(pid)
    else:
        raise SystemExit("Provide either a valid solution path (.py) or a numeric problem id")

    tests_path = args.tests
    if tests_path is None:
        if pid is None:
            raise SystemExit("--tests is required when problem id is not provided")
        tests_path = default_tests_path(pid)
    if not os.path.exists(tests_path):
        raise FileNotFoundError(f"Testcase file not found: {tests_path}")

    sol, module = load_solution(solution_path)
    method_name = choose_method(sol, args.method)

    with io.open(tests_path, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = split_testcases(content)
    if not blocks:
        raise SystemExit("No testcases found in file")

    print(f"Running: {os.path.relpath(solution_path)}::{method_name}")
    print(f"Tests:   {os.path.relpath(tests_path)} | {len(blocks)} case(s)\n")

    failures = 0
    for i, block in enumerate(blocks, 1):
        env, expected = parse_assignment_block(block)
        out, ok, msg = run_case(sol, method_name, env, expected, module)
        print(f"Case {i}: {out}")
        if expected is not None:
            print(f"  ✓ check: {ok}")
            if not ok:
                print(f"  {msg}")
                failures += 1

    if failures:
        raise SystemExit(f"{failures} testcase(s) failed")


if __name__ == "__main__":
    main()

