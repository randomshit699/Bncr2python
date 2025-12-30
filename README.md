# Bncr2python 

无界（Bncr）的python插件兼容层  
<img width="737" height="659" alt="image" src="https://github.com/user-attachments/assets/0ac60d1c-af60-454b-8b51-95bbf6cfdd30" />

# 安装  
## 1. 自动安装 
1.1 在无界web插件市场内订阅`https://github.com/randomshit699/Bncr_plugins`这个插件源  
1.2 安装源中的`python.ts` 插件  
1.3 重启无界`docker restart bncr`

## 2. 手动安装  
### 2.1 容器内安装python   
```sh
docker exec -it bncr sh  #进入无界容器内
apk update && apk upgrade  #更新包管理器
apk add python3=3.11.14-r0 py3-pip  #安装python和pip
exit  #退出容器
```
### 2.2 下载无界python兼容层  
下载  
[`__init__.py`](./__init__.py)  
[`python.cpython-311-x86_64-linux-musl.so`](./python.cpython-311-x86_64-linux-musl.so)  
这两个文件，保存到无界容器内同一个文件夹中（例如：`/bncr/src`）  
### 2.3 安装插件  
将[`python_manual.ts`](https://raw.githubusercontent.com/randomshit699/Bncr2python/refs/heads/main/python_manual.ts)插件下载至无界插件文件夹内 
### 2.4 重启无界  
```sh
docker restart bncr
```

# 使用说明  
## 1. 首次启动  
由于首次启动前需要pip install较多依赖，启动时间可能较长，当然你也可以在重启无界前在容器内自行安装
```sh
pip install -r requirements.txt --break-system-packages
```  
## 2. 插件加载  
兼容层启动后会自动创建`[Bncr_base]/plugin/python`作为插件目录，保存在此目录下的插件会被自动加载    
支持`*.py`|`*.so`插件  
文件名为`setup.py`或者以双下划线`__`开头的文件不会被加载，这是因为：  
仓库内的[`python/setup.py`](./python/setup.py)是使用cython一键编译插件目录以及子目录下所有`*.py`插件的脚本，原`*.py`会被重命名为`__*.py`    
`[Bncr_base]/plugin/python/configs`目录是用于借用无界的web插件设置页面的，不要在此目录下保存插件  
`[Bncr_base]/plugin/python/*/build`目录是cython编译时生成的，不要在此目录下保存插件  

## 3. type check
```python
if TYPE_CHECKING:
    from type.python import (
        BncrDB,
        BncrPluginConfig,
        MethodClass,
        Sender,
        router,
        sysMethod,
    )
```
[`python/type/python.pyi`](./python/type/python.pyi)  

# 开发文档  
## 1. 实现  
90%实现了无界在nodejs下的风格，语法可以参考[无界项目官网](https://anmours.github.io/Bncr/#/)，插件实例可以参考 [`python/__example.py`](./python/__example.py)与[`python/XJJ/__import_example.py`](./python/XJJ/__import_example.py)  
## 2. TODO 未实现  
1. Sender.Bridge()  [bncr]  
2. sysMethod.createStartupCompletionHook()  [bncr]  
3. sysMethod.isDevP()  [现在总是返回 false]
4. ADD `# @encrypt true`可以自动编译  [现在需要手动使用`setup.py`编译]
## 3. NOT TODO 不计划实现  
1. Adapter()  [bncr]

# 相关链接 
我：https://t.me/Gdot0  
无界项目官网：https://anmours.github.io/Bncr/#/  
无界tg群：https://t.me/BncrJSChat  
无界入门级教程：https://notes.dsdog.tk/archives/1716304583708  
