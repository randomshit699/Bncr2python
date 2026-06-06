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
    TypeVar,
    final,
)
from types import CoroutineType

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import APIRouter

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
    def __init__(
        self,
        watchInfo: "WatchInfo",
        oldValue: Any,
        newValue: Any,
        eventType: Literal["del", "set"],
    ) -> None: ...
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
    """Bncr内置数据库
    不支持后挂载数据库 即原new Bncr()的第二项参数"""

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
    .createStartupCompletionHook(唯一id, 函数, 参数)  #只启动完成后执行一次
    .createBncrConnectCompletionHook(唯一id, 函数, 参数)  #每次与Bncr建立连接后执行一次
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
    def createStartupCompletionHook(
        self, name: str, callback: Callable, args: tuple
    ) -> None: ...
    def createBncrConnectCompletionHook(
        self, name: str, callback: Callable, args: tuple
    ) -> None: ...
    def testModule(
        self, packages: List[str], install: bool = False
    ) -> Dict[str, bool]: ...
    async def sleep(self, second: Second): ...
    def getTime(self, format) -> str | int: ...
    async def inline(self, msg: str, name: str = "system@Admin"): ...
    async def push(
        self,
        platform: str,
        groupId: int | str,
        userId: int | str,
        msg: str,
        type: str = "text",
    ) -> str: ...
    async def pushAdmin(self, platform: list[str], msg: str): ...
    def isDev(self) -> bool: ...
    async def isDevP(self) -> bool: ...
    async def nodeRpc(self, filepath: str, method: str, *params: Any) -> Any:
        """sysMethod.nodeRpc
        远程调用node函数

        Args:
            filepath (str): (rel)"../xxx.js" || (abs)"/bncr/BncrData/xxx/yyy.js"
            method (str): (base)"" || (sub)"config" || (chain)"config.web.port"

        Example:
            await sysMethod.nodeRpc('../xxx.js', 'config.update', 'port', 1234)
        """
        ...

@final
class Sender:
    """Sender
    .reply如果需要定时删除，要提供delAfter参数
    .isAdmin需要await
    .Bridge(bridge, 参数)"""

    msgInfo: MessageInfo
    async def reply(self, msg: replyClass, delAfter: Second = 0) -> None: ...
    async def inlineSugar(self, msg: str) -> None: ...
    async def delMsg(self, msgIdArr: str | List[str]) -> None: ...
    async def waitInput(
        self,
        callback: Callable[[Sender], str | Sender | CoroutineType[Any, Any, Any]],
        time: Second,
    ) -> Sender | None: ...
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
    async def Bridge(self, bridge: str, *args) -> Any: ...

class nodeRpc:
    any_attr: Any
    async def __call__(*args: Any):
        if any(isinstance(arg, Callable) for arg in args):
            raise TypeError("nodeRpc错误: 无法传递函数作为参数")
        ...

def nodeImport(_from: str, *_import: str, submodule: Optional[str] = None) -> nodeRpc:
    """nodeImport
    import from node

    Args:
        _from (str): (rel)"../xxx.js" || (abs)"/bncr/xxx.js"
        _import (*str): 'get','set',...
        submodule (**Optional[str], optional): 'data.sql.api'. Defaults to None.

    Returns:
        nodeRpc: class nodeRpc
    """
    ...

sysMethod: SysMethod
router: APIRouter
