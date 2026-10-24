# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01 (Process Iteration Primitives)
"""L29 — 换档检测（非平稳适应）

零依赖，stdlib only。python impl.py 看 demo；python selftest.py 跑断言。
"""

import statistics

def l29_regime(before, after, z_threshold=2.0):
    """比较两段窗口的均值/方差，判定是否换档（regime shift）。"""
    if len(before) < 3 or len(after) < 3:
        return {"shift": None, "verdict": "insufficient"}
    m1, m2 = statistics.fmean(before), statistics.fmean(after)
    s1 = statistics.pstdev(before) or 1e-9
    s2 = statistics.pstdev(after) or 1e-9
    pooled = ((s1 ** 2 + s2 ** 2) / 2) ** 0.5
    z = (m2 - m1) / pooled if pooled else 0.0
    v_ratio = s2 / s1 if s1 else None
    shift = abs(z) >= z_threshold or (v_ratio is not None and (v_ratio >= 2 or v_ratio <= 0.5))
    return {
        "mean_before": round(m1, 4), "mean_after": round(m2, 4),
        "z": round(z, 3), "var_ratio": round(v_ratio, 3) if v_ratio else None,
        "shift": shift,
        "verdict": ("shift:均值动" if abs(z) >= z_threshold else "shift:波动动") if shift else "stationary",
        "action": "换档：旧阈值/旧权重全部要重标" if shift else "不换档：别动参数",
    }


def l29_demo():
    cases = {
        "平稳": ([1, 2, 3, 2, 1], [1, 2, 2, 3, 2]),
        "均值跳": ([1, 2, 3, 2, 1], [8, 9, 8, 9, 8]),
        "波动炸": ([2, 2, 2, 2, 2], [1, 9, 1, 9, 1]),
    }
    for k, (a, b) in cases.items():
        print("  %-4s -> %s" % (k, l29_regime(a, b)))


def l29_selftest():
    assert l29_regime([1, 2, 3, 2, 1], [8, 9, 8, 9, 8])["shift"] is True
    assert l29_regime([2, 2, 2, 2, 2], [1, 9, 1, 9, 1])["shift"] is True
    assert l29_regime([1, 2, 3, 2, 1], [1, 2, 2, 3, 2])["shift"] is False
    assert l29_regime([1], [2])["verdict"] == "insufficient"
    return True


if __name__ == "__main__":
    l29_demo()
