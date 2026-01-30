#!/usr/bin/env python3
"""Quantum FizzBuzz — a playful probabilistic take on the classic.

Usage:
  python3 quantum_fizz.py N [--seed SEED]

Behavior:
- For each i in 1..N compute base probabilities:
    base_fizz = 0.9 if i%3==0 else 0.15
    base_buzz = 0.9 if i%5==0 else 0.10
  Then add a small random noise in [-0.1, 0.1], clamp to [0,1].
- Sample to decide whether "Fizz" and/or "Buzz" occur.
- If both occur -> "FizzBuzz", if one -> it with probability shown, else the number.
- Deterministic when passed a seed.
"""

import argparse
import random
import math
import sys
from typing import List, Tuple


def clamp(x: float) -> float:
    return max(0.0, min(1.0, x))


def probs_for(i: int, rnd: random.Random) -> Tuple[float, float]:
    base_fizz = 0.9 if i % 3 == 0 else 0.15
    base_buzz = 0.9 if i % 5 == 0 else 0.10
    noise_f = rnd.uniform(-0.1, 0.1)
    noise_b = rnd.uniform(-0.1, 0.1)
    p_f = clamp(base_fizz + noise_f)
    p_b = clamp(base_buzz + noise_b)
    return p_f, p_b


def decide(i: int, rnd: random.Random) -> str:
    p_f, p_b = probs_for(i, rnd)
    is_f = rnd.random() < p_f
    is_b = rnd.random() < p_b
    # include probabilities for clarity
    pf = f"{p_f:.2f}"
    pb = f"{p_b:.2f}"
    if is_f and is_b:
        return f"FizzBuzz(F={pf},B={pb})"
    if is_f:
        return f"Fizz({pf})"
    if is_b:
        return f"Buzz({pb})"
    return str(i)


def run(n: int, seed: int | None = None) -> List[str]:
    rnd = random.Random(seed)
    out = [decide(i, rnd) for i in range(1, n + 1)]
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(description='Quantum FizzBuzz')
    parser.add_argument('n', type=int)
    parser.add_argument('--seed', type=int, default=None)
    args = parser.parse_args(argv)
    for line in run(args.n, args.seed):
        print(line)


if __name__ == '__main__':
    main()
