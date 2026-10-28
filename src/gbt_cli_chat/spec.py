"""The capability contract, copied verbatim from the GBT V8 registry.

Do not hand-edit: ``tests/test_spec.py`` pins every field against the
registry snapshot so drift fails the build instead of shipping quietly.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

_RAW = r"""{
 "name": "cli_chat",
 "domain": "integration",
 "desc": "外部 CLI 助手**对话面板**（把「集成」面板真的接到对话上）：`agents` 只读底表（装没装/版本/**能不能一次性驱动**/一次形态）· `send` **真发一句话**给选定的 CLI 助手（claude `-p` / codebuddy `-p` / codex `exec` / copilot `-p`，形态**现跑 --help 亲验**）· `transcript` 会话账 · `verify`/`where`。**「免费」的确切含义**：走各 CLI **自己的登录态/额度**（订阅额度），不经框架 API key ⇒ **不吃 API 账单**（≠ 无额度上限）。⚠️ 与 freebuff 的**本质差别**：这 4 位**都有**非交互一次性入口（freebuff 是 TUI-only）⇒ 面板**能真聊**。⚠️ `send` = 起外部进程 + 把 prompt 送出本机 ⇒ 挂 `process_execute`+`external_llm`；policy.py 无本位分支（owner-only，AI 无权改）⇒ 门在模块内自闸（auth_gate 唯一校验入口），缺授权如实报缺。未装位/图形位 fail-closed 如实报缺 + 给装法，**不编**。safe=false：send 起进程且内容出本机（不是纯只读面）。type=internal",
 "handler": "cli_chat",
 "safe": false,
 "external": false,
 "requires_params": false,
 "params": [],
 "params_hint": "",
 "multi_op": false,
 "ops": [],
 "ops_hint": ""
}"""


@dataclass(frozen=True)
class CapSpec:
    """Immutable description of one capability bit."""

    name: str
    domain: str
    desc: str
    handler: str
    safe: bool
    external: bool
    requires_params: bool
    params: Tuple[str, ...] = ()
    params_hint: str = ""
    multi_op: bool = False
    ops: Tuple[str, ...] = ()
    ops_hint: str = ""

    @property
    def gated(self) -> bool:
        """True when the registry marks this bit ``safe: false``.

        Gated does not mean "dangerous"; it means the action can change state
        that cannot be restored by running the inverse action.
        """
        return not self.safe

    @property
    def summary(self) -> str:
        """First clause of the description, for one-line listings."""
        for sep in ("\uff08", "\uff1b", "\u3002", ";"):
            if sep in self.desc:
                head = self.desc.split(sep, 1)[0].strip()
                if head:
                    return head
        return self.desc.strip()

    def as_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "domain": self.domain,
            "desc": self.desc,
            "handler": self.handler,
            "safe": self.safe,
            "gated": self.gated,
            "external": self.external,
            "requires_params": self.requires_params,
            "params": list(self.params),
            "params_hint": self.params_hint,
            "multi_op": self.multi_op,
            "ops": list(self.ops),
            "ops_hint": self.ops_hint,
        }


_data = json.loads(_RAW)

SPEC = CapSpec(
    name=_data["name"],
    domain=_data["domain"],
    desc=_data["desc"],
    handler=_data["handler"],
    safe=_data["safe"],
    external=_data["external"],
    requires_params=_data["requires_params"],
    params=tuple(_data["params"]),
    params_hint=_data["params_hint"],
    multi_op=_data["multi_op"],
    ops=tuple(_data["ops"]),
    ops_hint=_data["ops_hint"],
)
