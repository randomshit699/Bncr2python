r"""
# @author XJJ
# @name example
# @team XJJ
# @version 1.0.0
# @platform ['tgBot', 'HumanTG', 'ssh']
# @rule ^show example ([\s\S]+)$
# @rule ^tutorial$
# @description 插件编写基本说明，尽力还原无界语法了 ：》
# @admin True
# @disable False
# @classification ["Default", "System"]
# @service False
# @priority 99999
# @cron 0 */2 * * *
"""

# 注释头格式参考，注意开头三引号前面有个r
# author name team version description classification priority是必填的
# cron是5位crontab格式
# 也可以通过文末的方式来提供注释头

# 使用.pyi进行IDE提示
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from type.python import (  # type: ignore
        BncrDB,
        BncrPluginConfig,
        MethodClass,
        Sender,
        router,
        sysMethod,
    )

# BncrPluginConfig
jsonSchema = {"type": "object", "title": "jsonSchema示例", "description": "描述文本", "properties": {}}
ConfigDB = BncrPluginConfig(jsonSchema)


# 响应消息（@rule）的插件和注释头中设置了定时@cron的插件必须有 async def main(s: Sender
async def main(s: "Sender"):
    if s.getFrom() == "cron":
        print("cron trigger")
        return
    try:
        userConfig = await ConfigDB.get()
        print("userConfig", userConfig)

        # BncrDB
        db = BncrDB("system")
        await db.set("str", "text")
        await db.set("array", ["array"])
        await db.set("number", 9)
        t = await db.get("dict", {})
        k = await db.keys()
        print(t, k)

        async def watchCallback(method: MethodClass):
            print(f"{method.watchInfo.key} 发生 {method.eventType}, {method.oldValue}->{method.newValue}")
            if int(method.newValue) < 0:
                method.stop()
            elif int(method.newValue) == 0:
                await method.changeValue(99)
            else:
                print("不阻止此次修改")

        await db.watch({"id": "watch9", "callback": watchCallback, "key": "str"})
        await db.unwatch({"id": "watch9", "key": "str"})

        # sysMethod
        await sysMethod.sleep(3)
        time = sysMethod.getTime("%d/%m/%Y, %H:%M:%S")  # 等价于datetime.strftime(format)
        bncrDev = sysMethod.isDev()
        pythonDev = await sysMethod.isDevP()
        sysMethod.pipInstall(["httpx", "loguru", "fastapi"], mode="all")
        sysMethod.testModule(["uvicorn", "apscheduler"], install=True)
        # sysMethod.cron 基于 apscheduler.schedulers.background
        print(time, bncrDev, pythonDev)

        # Sender
        msg = s.getMsg()
        admin = await s.isAdmin()
        await s.reply("reply", delAfter=30)
        await s.delMsg(s.getMsgId())
        i = await s.waitInput(lambda s: "again" if s.getMsg() == "0" else "", 60)
        imsg = i.getMsg() if i else "no_input"
        p1 = s.param(1) or "no_param"
        s.setMsg("888")
        print(msg, admin, imsg, p1)

        return "next"
    except Exception as e:
        print(e)


# router 基于FastAPI.APIRouter，挂载到无界/python子路径下，比如这个例子会挂载到/python/status
@router.get("/status")
async def status():
    return "OK"


# 受限于无界，不支持挂载websocket
@router.websocket("/not_support")
async def ws():
    pass


# 加密插件可以通过编译为so实现
# 加密插件的注释头通过下面的方法提供（当然未编译的py源代码也可以这样，有注释头时优先使用注释头）
# fmt: off
__META_INFO__ = {"author": "XJJ",
                 "name": "example",
                 "team": "XJJ",
                 "version": "1.0.0",
                 "platform": ["tgBot", "HumanTG", "ssh"], # or None
                 "rule": [r'^show example ([\s\S]+)$', r'^tutorial$'], # or []
                 "description": '插件编写基本说明，尽力还原无界语法了 ：》',
                 "admin": True, # or False
                 "disable": False, 
                 "classification": ["Default", "System"], 
                 "service": False,
                 "priority": 99999,
                 "cron": '0 */2 * * *', # or None
                 }
# fmt: on
