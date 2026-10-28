# cli_chat

**One capability bit from GBT V8, packaged standalone.** No. 101 of 341,
`integration` domain (Integration).

<p>
<img alt="python" src="https://img.shields.io/badge/python-3.9%2B-blue">
<img alt="license" src="https://img.shields.io/badge/license-MIT-green">
<img alt="deps" src="https://img.shields.io/badge/runtime%20dependencies-0-brightgreen">
</p>

> 外部 CLI 助手**对话面板**（把「集成」面板真的接到对话上）：`agents` 只读底表（装没装/版本/**能不能一次性驱动**/一次形态）· `send` **真发一句话**给选定的 CLI 助手（claude `-p` / codebuddy `-p` / codex `exec` / copilot `-p`，形态**现跑 --help 亲验**）· `transcript` 会话账 · `verify`/`where`。**「免费」的确切含义**：走各 CLI **自己的登录态/额度**（订阅额度），不经框架 API key ⇒ **不吃 API 账单**（≠ 无额度上限）。⚠️ 与 freebuff 的**本质差别**：这 4 位**都有**非交互一次性入口（freebuff 是 TUI-only）⇒ 面板**能真聊**。⚠️ `send` = 起外部进程 + 把 prompt 送出本机 ⇒ 挂 `process_execute`+`external_llm`；policy.py 无本位分支（owner-only，AI 无权改）⇒ 门在模块内自闸（auth_gate 唯一校验入口），缺授权如实报缺。未装位/图形位 fail-closed 如实报缺 + 给装法，**不编**。safe=false：send 起进程且内容出本机（不是纯只读面）。type=internal

That description is copied verbatim from the registry. `tests/test_spec.py` pins it,
so documentation drift fails the build instead of shipping quietly.

## What this package actually is

It is the **contract** for one capability: its name, its parameters, the values it
accepts, and whether it can change state that cannot be restored. It is not the
implementation — that lives in the runtime this bit was extracted from.

So `run()` goes through a narrow `Backend` protocol, and the default backend is a
stub that **says so**:

```
status="validated"   backend="stub"   data={"executed": false}
```

Never `status="ok"`. A stub that reports success is worse than no stub, because the
caller stops looking for the real thing.

## Install

```bash
git clone https://github.com/gbtweilai-star/gbt-cli-chat.git
cd gbt-cli-chat
python -m pip install -e ".[dev]"
```

## Use

```bash
python -m gbt_cli_chat info                  # capability card
python -m gbt_cli_chat spec --json           # machine-readable contract
python -m gbt_cli_chat check --payload '{}'
python -m gbt_cli_chat run   --payload '{}'
```

Real `info` output from this machine:

```text
cli_chat  (integration)  v1.0.0
----------------------------------------
外部 CLI 助手**对话面板**（把「集成」面板真的接到对话上）：`agents` 只读底表（装没装/版本/**能不能一次性驱动**/一次形态）· `send` **真发一句话**给选定的 CLI 助手（claude `-p` / codebuddy `-p` / codex `exec` / copilot `-p`，形态**现跑 --help 亲验**）· `transcript` 会话账 · `verify`/`where`。**「免费」的确切含义**：走各 CLI **自己的登录态/额度**（订阅额度），不经框架 API key ⇒ **不吃 API 账单**（≠ 无额度上限）。⚠️ 与 freebuff 的**本质差别**：这 4 位**都有**非交互一次性入口（freebuff 是 TUI-only）⇒ 面板**能真聊**。⚠️ `send` = 起外部进程 + 把 prompt 送出本机 ⇒ 挂 `process_execute`+`external_llm`；policy.py 无本位分支（owner-only，AI 无权改）⇒ 门在模块内自闸（auth_gate 唯一校验入口），缺授权如实报缺。未装位/图形位 fail-closed 如实报缺 + 给装法，**不编**。safe=false：send 起进程且内容出本机（不是纯只读面）。type=internal

gated      : True   <- needs explicit consent
external   : False
multi-op   : False
params     : (none)
```

Wire a real implementation:

```python
from gbt_cli_chat import run

class MyBackend:
    name = "my-backend"
    def invoke(self, cap, payload):
        return {"cap": cap, "handled": sorted(payload)}

result = run({}, backend=MyBackend())
assert result.status == "ok"
```

## Parameters

| name | required | notes |
|---|---|---|
| — | no | the registry declares no required parameters |

Registry hint (`params_hint`): (empty)

Types are deliberately absent: the registry does not declare them, and an invented
type is worse than no type, because callers believe it.

## Boundaries

- Gated: this bit is marked `safe: false` in the registry — it can change state that no inverse action restores.
- No external service dependency declared.
- Single-action bit.
- No implementation ships here. Bring a backend; the protocol is one method.

## What this is not

Not a wrapper around a hosted API. Not a model. Not a promise that calling it does
anything on its own. It is the typed seam plus the validation, which is the part that
stays correct even when the implementation changes.

## Tests

```bash
python -m pytest
```

```text
20 passed, 3 skipped in 0.11s
```

## Provenance

| field | value |
|---|---|
| capability | `cli_chat` |
| domain | `integration` |
| handler | `cli_chat` |
| safe | `False` (gated = `True`) |
| external | `False` |
| atlas page | [integration/cli_chat](https://github.com/gbtweilai-star/gbt-caps/blob/main/caps/integration/cli_chat.md) |
| full index | [https://github.com/gbtweilai-star/gbt-caps](https://github.com/gbtweilai-star/gbt-caps) |

The parent README says 348 capabilities; an AST pass over the registry enumerates
`341 + 0 unimplemented + 0 disabled = 341`. The extra 7 are historical duplicates.
Numbering here follows 341 and matches the `gbt-caps` index one-to-one.

## License

MIT.
