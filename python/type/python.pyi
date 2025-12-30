from dataclasses import dataclass, field
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Literal,
    NotRequired,
    Optional,
    Required,
    TypedDict,
    Union,
    final,
)

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

type Second = int

class ReplyInfoDict(TypedDict, total=False):
    """Reply消息体字典"""

    type: Required[str]
    msg: Required[str]
    userId: Required[str]
    groupId: Required[str]
    path: NotRequired[str]
    toMsgId: NotRequired[str]

@dataclass
class ReplyInfo:
    """Reply消息体类"""

    type: str
    msg: str
    userId: str
    groupId: str
    path: Optional[str] = None
    toMsgId: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: ReplyInfoDict) -> "ReplyInfo": ...
    def to_dict(self) -> "ReplyInfoDict": ...

type replyClass = Union[ReplyInfoDict, ReplyInfo, str]

@final
class MessageInfo:
    """Sender.msgInfo类"""

    userId: str
    friendId: str
    userName: str
    groupId: str
    groupName: str
    msg: str
    msgId: str
    replyToMsgId: str
    from_: str
    rule: str

@final
class MethodClass:
    """BncrDB watch的callback中接收的method参数
    newValue: key即将被修改为的值
    oldValue: key旧值"""

    newValue: Any
    oldValue: Any
    eventType: Literal["del", "set"]
    watchInfo: WatchInfo
    def __init__(self, watchInfo: "WatchInfo", oldValue: Any, newValue: Any, eventType: Literal["del", "set"]) -> None: ...
    def stop(self) -> None:
        """停止callback (执行过changeValue())
        或者恢复oldValue (else)"""
        ...

    async def changeValue(self, newValue: Any) -> None:
        """篡改newValue
        不要在callback中使用BncrDB.set，会循环被watch"""
        ...

class WatchInfoDict(TypedDict):
    """BncrDB.watch的参数字典"""

    id: Required[str]
    callback: NotRequired[Callable[[MethodClass], Any]]
    key: Required[str]

@final
class WatchInfo:
    """BncrDB.watch的参数类"""

    db: "BncrDB"
    id: str
    key: str

class BncrDB:
    """BncrDB"""

    name: str

    def __init__(self, name: str) -> None: ...
    async def get(self, key: str, returnVal: Any = None) -> Any: ...
    async def set(self, key: str, value: Any) -> bool: ...
    async def del_(self, key: str) -> bool: ...
    async def keys(self) -> list[str]: ...
    async def getAllForm(self) -> list[str]: ...
    async def watch(self, watchInfo: WatchInfoDict) -> bool: ...
    async def unwatch(self, watchInfo: WatchInfoDict) -> bool: ...

class BncrPluginConfig:
    """BncrPluginConfig
    可以await创建，但是好像没什么大用"""

    userConfig: Dict
    jsonSchema: Any
    def __init__(self, jsonSchema: Any) -> None: ...
    def __await__(self, jsonSchema: Any) -> "BncrPluginConfig": ...
    async def get(self): ...

@final
class SysMethod:
    """SysMethod
    .cron语法请查看AsyncIOScheduler的文档
    .npmInstall改成了.pipInstall
    .isDev继承无界的超授权限
    .isDevP是我的
    .createStartupCompletionHook还没实现
    """

    cron: AsyncIOScheduler
    MachineId: str
    config: Dict
    Version: str
    osPlatform: str
    systemConfig: Dict
    def pipInstall(
        self,
        packages: List[str] | str,
        mode: Literal["silent", "error", "all", "capture"] = "error",
    ) -> tuple[str, str] | bool: ...
    def createStartupCompletionHook(self, name, callback) -> None: ...
    def testModule(self, packages: List[str], install: bool = False) -> Dict[str, str]: ...
    async def sleep(self, second: Second): ...
    def getTime(self, format) -> str | int: ...
    async def inline(self, msg: str, name: str = "system@Admin"): ...
    async def push(self, platform: str, groupId: int | str, userId: int | str, msg: str, type: str = "text") -> str: ...
    async def pushAdmin(self, platform: list[str], msg: str): ...
    def isDev(self) -> bool: ...
    async def isDevP(self) -> bool: ...

@final
class Sender:
    """Sender
    .reply如果需要定时删除，要提供delAfter参数
    .isAdmin需要await
    .Bridge还没实现"""

    msgInfo: MessageInfo
    async def reply(self, msg: replyClass, delAfter: Second = 0) -> None: ...
    async def inlineSugar(self, msg: str) -> None: ...
    async def delMsg(self, msgIdArr: str | List[str]) -> None: ...
    async def waitInput(self, callback: Callable[[Sender], str | Sender], time: Second) -> Sender | None: ...
    async def again(self, msg: replyClass) -> Sender | None: ...
    def param(self, k: int) -> str: ...
    def getMsg(self) -> str: ...
    def setMsg(self, msg: Any) -> None: ...
    def getUserId(self) -> str: ...
    def getUserName(self) -> str: ...
    def getGroupId(self) -> str: ...
    def getGroupName(self) -> str: ...
    def getFrom(self) -> str: ...
    def getMsgId(self) -> str: ...
    async def isAdmin(self) -> bool: ...
    async def Bridge(self, *args) -> Any: ...

sysMethod: SysMethod
router: FastAPI
