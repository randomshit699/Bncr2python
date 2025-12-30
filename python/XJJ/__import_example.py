r"""
# @author XJJ
# @name import_example
# @team XJJ
# @version 1.0.0
# @platform ['tgBot', 'HumanTG', 'ssh']
# @rule ^impt$
# @description import包的一些注意事项
# @admin True
# @disable False
# @classification ["Default", "System"]
# @service False
# @priority 99999
"""

# ruff: noqa: F401
from typing import TYPE_CHECKING

from XJJ.util import tool  # 使用基于/python目录的绝对路径导包

# 尽可能将被依赖的模块放到深层文件夹下，尽可能按依赖性由重到轻的顺序排序模块名，这与加载顺序有关


if TYPE_CHECKING:
    from type.python import (
        BncrDB,
        BncrPluginConfig,
        MethodClass,
        Sender,
        router,
        sysMethod,
    )


async def main(s: Sender):

    tool.tool_hello(s.getMsg())


# fmt: off
__META_INFO__ = {"author": "XJJ",
                 "name": "import_example",
                 "team": "XJJ",
                 "version": "1.0.0",
                 "platform": ["tgBot", "HumanTG", "ssh"], # or None
                 "rule": [r'^impt$'], # or []
                 "description": 'import包的一些注意事项',
                 "admin": True, # or False
                 "disable": False, 
                 "classification": ["Default", "System"], 
                 "service": False,
                 "priority": 99999,
                 "cron": None, # or None
                 }
# fmt: on
