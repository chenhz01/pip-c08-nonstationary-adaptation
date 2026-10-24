# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01 (Process Iteration Primitives)
"""L30 — 适应速率闸（非平稳适应）

零依赖，stdlib only。python impl.py 看 demo；python selftest.py 跑断言。
"""


def l30_rate(n_new, n_old, max_step=0.5):
    """新样本相对旧经验的权重上限。

    直方图式的朴素做法是「新证据全信」，它在样本很少时会整体翻车；
    这里给的是 n/(n+k) 型衰减 + 上限封顶，k 固定为 10（先验强度）。
    """
    if n_new <= 0:
        return {"weight_new": 0.0, "verdict": "no-new-evidence"}
    k = 10.0
    raw = n_new / (n_new + k)
    if n_old <= 0:
        raw = max(raw, 0.5)
    w = min(raw, max_step)
    return {
        "weight_new": round(w, 3),
        "weight_old": round(1 - w, 3),
        "raw": round(raw, 3),
        "capped": raw > max_step,
        "verdict": "新证据不足以推翻旧结论" if w < 0.3 else ("需要双轨并行观察" if w < 0.5 else "可以更新主结论"),
        "note": "上限 %.2f 是防「用一个坏样本改掉整套经验」的闸" % max_step,
    }


def l30_demo():
    for n in (1, 3, 10, 30, 100):
        print("  新样本%3d 条 -> %s" % (n, l30_rate(n, 50)))


def l30_selftest():
    assert l30_rate(0, 10)["verdict"] == "no-new-evidence"
    assert l30_rate(100, 10)["capped"] is True and l30_rate(100, 10)["weight_new"] == 0.5
    assert l30_rate(1, 50)["weight_new"] < 0.3
    assert l30_rate(5, 0)["weight_new"] >= 0.3
    return True


if __name__ == "__main__":
    l30_demo()
