# MechManual

面向车间维护的**设备手册问答**工具。把泵、风机、减速机一类手册切成可检索片段，用关键词先能查到条款；后续接入向量检索、DeepSeek 生成和 MCP，给现场和 IDE 里的 Agent 用。

向量检索 MCP 底座见独立仓库 [mcp-vector](https://github.com/xrykmb/mcp-vector)（HNSW + 元数据过滤 + MCP tools）。

## 解决什么问题

纸质/PDF 手册难搜：术语不统一（「润滑周期」vs「加油间隔」），现场要翻很久。典型用法：维修时问「这台离心泵多久换脂」，系统返回手册原文所在章节，而不是凭印象作答。

## 技术栈

| 层 | 当前 | 规划 |
|----|------|------|
| 语言 | Python 3.11+ | 同左 |
| 检索 | 章节切分 + 关键词打分 | 对接 mcp-vector 的 HNSW |
| 生成 | 未接（骨架阶段） | DeepSeek OpenAI 兼容接口 |
| 协议 | CLI | MCP tools：`search_manual` / `ask_manual` |

## 架构

```
examples/manuals/*.md  →  parse sections  →  score(query)  →  CLI
                                              ↘ 后续：mcp-vector + LLM
```

`src/mechmanual/` 只放可测试的纯逻辑，CLI 很薄，方便后面加 MCP 而不改检索核心。

## 快速启动

需要 Python 3.11+（3.10 一般也可）。

```powershell
git clone https://github.com/xrykmb/mechmanual.git
cd mechmanual
python -m venv .venv
.\ .venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
mechmanual search "润滑" --manuals examples/manuals
python -m pytest
```

Linux/macOS 把激活换成 `source .venv/bin/activate`。

复制 `.env.example` 为 `.env` 后填写 key（生成模块接上之后才会用到）。

## 演示示例

仓库自带一份离心泵维护样例：

```text
mechmanual search "轴承过热"
```

应能命中「故障与处理」章节，并打印来源路径。

## 未来规划

- [ ] 手册切分结果写入 [mcp-vector](https://github.com/xrykmb/mcp-vector)
- [ ] DeepSeek 带依据的生成（只引用检索到的条款）
- [ ] MCP Server，供 Cursor / Claude 调用手册检索
- [ ] 领域同义词表（润滑/加油/脂）

## License

MIT
