#!/usr/bin/env python3
"""
Simplest local runner for LeetCode-style Python solutions.

Usage:
  # Run by problem id; uses tests/<id>.txt
  python tools/lc.py 0001

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
    # Return Solution instance when available; otherwise None (for design problems)
    sol = module.Solution() if hasattr(module, "Solution") else None
    return sol, module


def choose_method(sol, forced: str | None = None) -> str:
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
    # Design problems: ops/args drive class methods (e.g., MinStack)
    if "ops" in env and "args" in env:
        ops = env["ops"]
        args_list = env["args"]
        if not isinstance(ops, list) or not isinstance(args_list, list) or len(ops) != len(args_list):
            raise ValueError("ops and args must be lists of equal length")
        class_name = ops[0]
        if not hasattr(module, class_name):
            raise AttributeError(f"Class '{class_name}' not found in solution module")
        cls = getattr(module, class_name)
        inst = cls(*args_list[0])
        outputs = [None]
        for op, a in zip(ops[1:], args_list[1:]):
            m = getattr(inst, op)
            res = m(*a)
            outputs.append(res if res is not None else None)
        ok = True
        msg = ""
        if expected is not None:
            ok = outputs == expected
            if not ok:
                msg = f"Expected {expected}, got {outputs}"
        return outputs, ok, msg

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
    if listnode_cls is not None:
        if out is None:
            shown_out = []
        elif hasattr(out, "next") and hasattr(out, "val"):
            shown_out = listnode_to_list(out)

    # In-place problems that return None: compare mutated first list arg
    if out is None and expected is not None:
        for val in env.values():
            if isinstance(val, list):
                shown_out = val
                break

    ok = True
    msg = ""
    if expected is not None:
        # Equality helper with float tolerance and list recursion
        def eq(a, b):
            # list/tuple
            if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
                if len(a) != len(b):
                    return False
                return all(eq(x, y) for x, y in zip(a, b))
            # numbers (int/float)
            if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                # If either is float, compare with tolerance
                if isinstance(a, float) or isinstance(b, float):
                    return abs(float(a) - float(b)) <= 1e-9
                return a == b
            # fallback
            return a == b

        cmp_left = shown_out if shown_out is not out else out

        # Normalize list-of-lists outputs (e.g., anagram groups) by
        # sorting inner lists and then the outer list.
        def is_list_of_lists(x):
            return isinstance(x, list) and (len(x) == 0 or isinstance(x[0], (list, tuple)))

        if is_list_of_lists(cmp_left) and is_list_of_lists(expected):
            def norm(lst):
                return sorted([tuple(sorted(inner)) for inner in lst])
            cmp_left = norm(cmp_left)
            expected = norm(expected)
        ok = eq(cmp_left, expected)
        if not ok:
            msg = f"Expected {expected}, got {shown_out}"
    return shown_out, ok, msg


def main():
    ap = argparse.ArgumentParser(description="Run LeetCode-style Python Solution locally (by id)")
    ap.add_argument("id", help="Problem id (e.g., 1 or 0001)")
    args = ap.parse_args()

    if not is_problem_id(args.id):
        raise SystemExit("Please provide a numeric problem id, e.g., 0001")

    pid = args.id.zfill(4)
    solution_path = find_solution_by_id(pid)
    tests_path = default_tests_path(pid)
    if not os.path.exists(tests_path):
        raise FileNotFoundError(f"Testcase file not found: {tests_path}")

    sol, module = load_solution(solution_path)
    method_name = choose_method(sol) if sol is not None else None

    with io.open(tests_path, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = split_testcases(content)
    if not blocks:
        raise SystemExit("No testcases found in file")

    label = f"{os.path.relpath(solution_path)}::{method_name}" if method_name else os.path.relpath(solution_path)
    print(f"Running: {label}")
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
