# cztDevDemos
自制的一些demo用于展示原理,提供简单的代码框架供复用:  

【gcc中dll动态和静态链接demo】  
环境:Windows GUN(g++,gcc) 
展示了如何构建一个独立的dll其中包含了一个独立的函数和类,staticmain.cpp
和dynamicmain.cpp分别从动态和静态两种方法来调用生成的dll中的函数和类

【PasswordManage】  
环境:Windows VisualStudio2022  
展示了如何在winform中的panel容器中批量生成控件,
并将account结构中的账号展示在批量生成的button中,按
下对应的button将对应的密码复制到剪贴板上

【YDsender】  
环境:Windows VisualStudio2022  
实现了将模拟浏览器请求有道翻译的post,并获取翻译的结果,
展示了如何在winform(C#下)中发送一个POST请求并建立session最后到翻译获取response,
通过MD5,AES解码加密的response的结果,
通过Json解析解密后的文本建立json对象,并发送到textbox中。

【cmakedemo】   
环境:Windows GUN(g++,gcc,mingw32-make) cmake 
注：确保你将MinGW/bin/mingw32-make.exe 复制一份并改名为make.exe  
提供两份样例。
single样例用命令编译(command在cmakelist.txt中)演示了一个包含头文件的代码如何编译。
multi样例将gcc中dll动态链接demo改造成用cmake形式编译,运行compiler.ps1即可在biuld/output/bin中找到可执行文件。

【Python控制台小游戏】
环境:Windows Python 3.10
实现了一个仿照魔塔的控制台小游戏 
因为历史原因所有的代码都写在dev.py,还没有拆出来(因为这是作业代码不让拆开写...)  
`$ python ./dev.py`即可  
完成了基本的的Prefab抽象  
完成了Prefa对象间的Action机制  
完成了基本的Animation渲染功能    
完成了基本的Event广播机制   
完成了动态加载UI(Widget)机制  
完成了动态加载地图机制  
通过json实现了基本的数据存储机制  
完成了了地图/动画资源的储存与运行代码的解耦  
完成了一个地图资源编辑器srcedit.py 
11-8：拆开改了一遍,现在勉强能看了，py写大一点的东西真是折磨，key_handler还要再改改，以后再说吧...

【PyQt5统计信息熵demo】
环境:Windows pyqt5-lite python 3.8 Embeding
一个用pystand封装的pyqt项目  
可以统计文本信息熵  

【Math】
环境:Windows python各种包
一些独立的数学小实例

【cztBlueTools】
环境：.NetFramework4.8 winform
一个利用winform自制的小工具合集
可以自动化批量截图

