# fmt: off
__META_INFO__ = {"author": "XJJ",
                 "name": "tool",
                 "team": "XJJ",
                 "version": "1.0.0",
                 "platform": None,
                 "rule": [],
                 "description": '工具模块',
                 "admin": False,
                 "disable": False, 
                 "classification": ["Default", "System"], 
                 "service": False,
                 "priority": 99999,
                 "cron": None,
                 }
# fmt: on


def tool_hello(msg):
    print(f"tool_hello -> {msg}")
