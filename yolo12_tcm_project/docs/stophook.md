# StopHook 守门说明

用户要求：只有当 agent 输出以下短语时才允许停止：

`我绝对确定所有任务都已经完成且所有目标都已经达成`

## 已实现内容

项目内已提供守门脚本：

`scripts/stop_guard.py`

该脚本会从 hook 标准输入、JSON 字段、`transcript_path` 指向的记录文件中搜索指定短语。若未找到该短语，脚本以退出码 `2` 返回，并输出阻止停止的说明。

## Claude Code 示例配置

如果运行环境支持 Claude Code hooks，可将以下配置放入项目根目录的 `.claude/settings.local.json`：

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "\"D:\\\\AAA中药cv\\\\yolo12_tcm_project\\\\.venv\\\\Scripts\\\\python.exe\" \"D:\\\\AAA中药cv\\\\yolo12_tcm_project\\\\scripts\\\\stop_guard.py\""
          }
        ]
      }
    ]
  }
}
```

## 当前限制

当前 Codex 桌面线程没有暴露可直接注册 StopHook 的工具或 API。因此本项目已提供可执行守门脚本和 Claude Code 配置示例，但不能伪称已经控制 Codex 桌面客户端本身的停止机制。

最终回答中，只有当所有任务确实完成并且所有目标达成时，才允许输出上述完成短语。
