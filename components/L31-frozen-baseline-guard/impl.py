# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01 (Process Iteration Primitives)
"""L31 — 冻结基线守卫（非平稳适应）

零依赖，stdlib only。python impl.py 看 demo；python selftest.py 跑断言。
"""

import zlib

def l31_seal(baseline_text, version):
    return {"version": version, "digest": "%08x" % zlib.crc32(baseline_text.encode())}


def l31_check(seal, current_text, approved_version=None):
    """检测「悄悄改基准」：内容变了但版本没变 → 红旗。"""
    cur = "%08x" % zlib.crc32(current_text.encode())
    changed = cur != seal["digest"]
    version_ok = (approved_version is not None and approved_version != seal["version"])
    if not changed:
        return {"changed": False, "verdict": "sealed", "note": "基线未动"}
    if changed and not version_ok:
        return {"changed": True, "verdict": "tampered",
                "note": "内容已变但版本号未升：这是最危险的一种「改进」"}
    return {"changed": True, "verdict": "approved-change",
            "note": "有显式批准：版本 %s -> %s，可复算" % (seal["version"], approved_version)}


def l31_demo():
    s = l31_seal("baseline v1", "1.0")
    print("  未动 ->", l31_check(s, "baseline v1"))
    print("  偷改 ->", l31_check(s, "baseline v1 (relaxed)"))
    print("  批准 ->", l31_check(s, "baseline v1 (relaxed)", approved_version="1.1"))


def l31_selftest():
    s = l31_seal("x", "1.0")
    assert l31_check(s, "x")["verdict"] == "sealed"
    assert l31_check(s, "y")["verdict"] == "tampered"
    assert l31_check(s, "y", approved_version="1.1")["verdict"] == "approved-change"
    return True


if __name__ == "__main__":
    l31_demo()
