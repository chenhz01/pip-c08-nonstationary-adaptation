# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01 (Process Iteration Primitives)
"""L32 — 元搜索预算（非平稳适应）

零依赖，stdlib only。python impl.py 看 demo；python selftest.py 跑断言。
"""


def l32_successive_halving(candidates, budget_per_round, rounds=3, keep=0.5):
    """逐轮淘汰：每轮给存活候选均分预算，按得分保留前 keep 比例。

    candidates: [{"id","score"}]（score 可先验，也可在该轮被实测替换）
    返回每轮预算分配与淘汰顺序。
    """
    alive = [dict(c) for c in candidates]
    log = []
    for r in range(rounds):
        if len(alive) <= 1 or budget_per_round <= 0:
            break
        per = budget_per_round / len(alive)
        alive.sort(key=lambda c: -c["score"])
        n_keep = max(1, int(len(alive) * keep))
        cut = [c["id"] for c in alive[n_keep:]]
        log.append({"round": r + 1, "alive": [c["id"] for c in alive],
                    "per_candidate": round(per, 2), "cut": cut})
        alive = alive[:n_keep]
    return {"log": log, "winner": alive[0]["id"] if alive else None,
            "spent": round(sum(l["per_candidate"] * len(l["alive"]) for l in log), 2),
            "note": "淘汰赛的价值不是找最优，而是「用固定预算把不可信的先杀掉」"}


def l32_demo():
    cands = [{"id": "A", "score": 0.6}, {"id": "B", "score": 0.9},
             {"id": "C", "score": 0.4}, {"id": "D", "score": 0.7}]
    r = l32_successive_halving(cands, 400, rounds=3, keep=0.5)
    for l in r["log"]:
        print("  轮%d 存活%s 每人%.0f 淘汰%s" % (l["round"], l["alive"], l["per_candidate"], l["cut"]))
    print("  胜者 %s 花费 %.0f | %s" % (r["winner"], r["spent"], r["note"]))


def l32_selftest():
    r = l32_successive_halving([{"id": "A", "score": 0.6}, {"id": "B", "score": 0.9}], 400, rounds=3)
    assert r["winner"] == "B"
    assert r["log"][0]["cut"] == ["A"]
    assert l32_successive_halving([{"id": "Z", "score": 1}], 100)["winner"] == "Z"
    return True


if __name__ == "__main__":
    l32_demo()
