import json, urllib.request, urllib.error, time, os, subprocess

ROOT = r"F:\Tsinglin_Voice"
repos = [
    ("TTS", "TTS/qwentts.cpp", "ServeurpersoCom/qwentts.cpp"),
    ("TTS", "TTS/audio.cpp", "0xShug0/audio.cpp"),
    ("TTS", "TTS/ilaria-s2.cpp", "L9Tigrotto/ilaria-s2.cpp"),
    ("TTS", "TTS/voxcpm2-turkce-ses-tasarimi", "alexturkey/voxcpm2-turkce-ses-tasarimi"),
    ("TTS", "TTS/VoxCPM.cpp", "bluryar/VoxCPM.cpp"),
    ("TTS", "TTS/koboldcpp", "LostRuins/koboldcpp"),
    ("TTS", "TTS/CrispASR", "CrispStrobe/CrispASR"),
    ("LLM", "LLM/pascallama.cpp", "madsteph74/pascallama.cpp"),
    ("LLM", "LLM/minicpm5-kernel-pascal", "ArtyomITA/minicpm5-kernel-pascal"),
    ("LLM", "LLM/PrismML-llama.cpp", "PrismML-Eng/llama.cpp"),
    ("LLM", "LLM/bonsai2-ternary-pascal", "ArtyomITA/bonsai2-ternary-pascal"),
    ("LLM", "LLM/ik_llama.cpp", "ikawrakow/ik_llama.cpp"),
    ("ASR", "ASR/whisper.cpp", "ggml-org/whisper.cpp"),
    ("ASR", "ASR/sherpa-onnx", "k2-fsa/sherpa-onnx"),
    ("子模块", "TTS/qwentts.cpp/ggml", "ServeurpersoCom/ggml"),
]

def api(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "TsinglinVoice-version-audit",
        "Accept": "application/vnd.github+json",
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

results = []
for cat, local, full in repos:
    entry = {"category": cat, "local": local, "full": full,
             "github": "https://github.com/" + full, "status": "?"}
    local_dir = os.path.join(ROOT, local)
    if os.path.isdir(os.path.join(local_dir, ".git")):
        try:
            h = subprocess.check_output(
                ["git", "-C", local_dir, "rev-parse", "HEAD"],
                stderr=subprocess.DEVNULL).decode().strip()
            entry["local_head"] = h
        except Exception:
            entry["local_head"] = ""
    try:
        info = api("https://api.github.com/repos/" + full)
        br = info.get("default_branch", "main")
        entry["default_branch"] = br
        entry["pushed_at"] = info.get("pushed_at", "")
        entry["archived"] = info.get("archived", False)
        try:
            c = api("https://api.github.com/repos/%s/commits/%s" % (full, br))
            entry["upstream_commit"] = c.get("sha", "")
            entry["commit_date"] = c.get("commit", {}).get("committer", {}).get("date", "")
            entry["commit_msg"] = c.get("commit", {}).get("message", "").split("\n")[0][:90]
        except Exception as e:
            entry["commit_err"] = str(e)[:80]
        entry["status"] = "ok"
    except Exception as e:
        entry["status"] = "api_error: " + str(e)[:60]
        try:
            out = subprocess.check_output(
                ["git", "ls-remote", entry["github"] + ".git", "HEAD"],
                stderr=subprocess.DEVNULL, timeout=25).decode().strip()
            entry["upstream_commit"] = out.split()[0]
            entry["status"] = "lsremote"
        except Exception as e2:
            entry["status"] = "fail: " + str(e2)[:50]
    results.append(entry)
    print("%-14s %-42s br=%-10s sha=%s" % (
        entry["status"], full, entry.get("default_branch", "?"),
        entry.get("upstream_commit", "")[:12]), flush=True)
    time.sleep(0.4)

json.dump(results, open(os.path.join(ROOT, "_versions.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)

lines = [
    "# 仓库版本清单（GitHub 地址 + 版本号）",
    "",
    "审计时间（本地）：" + time.strftime("%Y-%m-%d %H:%M:%S"),
    "",
    "> 说明：带完整 git 的仓库记录本地 HEAD；zipball 下载的仓库无 .git，",
    "> 记录查询时刻**上游默认分支最新 commit**（下载时快照，若上游其后更新会有偏差）。",
    "",
    "| 类别 | 本地路径 | GitHub 地址 | 默认分支 | 上游最新 commit | 本地 HEAD | 版本管理 |",
    "|---|---|---|---|---|---|---|",
]
for e in results:
    lh = e.get("local_head", "")
    sha = e.get("upstream_commit", "")
    mgmt = "完整 git" if lh else "zipball(无.git)"
    lines.append("| %s | `%s` | %s | %s | `%s` | `%s` | %s |" % (
        e["category"], e["local"], e["github"], e.get("default_branch", "?"),
        sha[:12] if sha else "-", lh[:12] if lh else "-", mgmt))
lines += ["", "## commit 主题", ""]
for e in results:
    lines.append("- **%s** `%s` — %s" % (
        e["local"], e.get("upstream_commit", "")[:12],
        e.get("commit_msg", "") or e.get("pushed_at", "") or e.get("status", "")))
open(os.path.join(ROOT, "仓库版本清单.md"), "w", encoding="utf-8").write("\n".join(lines))
print("DONE -> 仓库版本清单.md / _versions.json", flush=True)
