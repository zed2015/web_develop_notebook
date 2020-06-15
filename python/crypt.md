### python 代码的加密
Python源码保护方式

基本原理

实现难度/成本

破解难度/成本

支持的语法/功能

Code Obfuscation/生成byte code

使用代码混淆或者python自带的一些module或工具，编译生成难读的python字节码(.pyc/.pyo)，从而达到隐藏源代码的目的

低。有现成的python库或者tools来生成byte code，例如compileall, py_compile，py2exe(for windows)等

低。也同样有现成的工具来反编译byte code成源代码，如： decompyle, uncompyle6等

Python全部语法都支持。

生成native code

通过先编译python源文件成C/C++源文件，然后再编译C/C++源文件为可执行文件的方式来隐藏源代码

中。有一些开源项目来帮助实现，如Cython，Shed Skin，Nuitka等，但是开发人员也要自己做一些工作。

高。C/C++源码编译生成的native code破解难度非常大，在目前的技术技术世界里，全部源码反向工程几乎不可能。

大部分python语法和数据类型都支持，Cython还有一些edge的caveats， 而Nuitka则宣称fully compatible with python。

 

 

基于以上的对比，显然我们要选择#2.

 

从上面的3个开源项目来对比：

 

项目

社区活跃度

Licensing

文档完整性

对于python的支持

未来规划

学习/使用成本

推荐建议

Cython

非常高。有240+contributors，13000+commits，且当前在持续更新中。

友好。采用Apache License,对于我们的知识产权无侵害。

好，文档非常完整。

好。常见语法和结构都支持(虽然有小的caveats)，对于python的版本支持也很完备。

目标明确，roadmap未披露。

中。Cython的目标是做一个python的超集，支持python和C的混编。

不建议。Cython的目标比较远大，对于我们的使用场景来说过于庞大，复杂。未来可持续关注。

Nuitka

高。有~30 contributors，~5000commits，且当前在持续更新中。

友好。采用Apache License,对于我们的知识产权无侵害。

好，用户文档和开发文档都很完善。

好。宣称fully compatible with python。

目标明确，roadmap清晰，目前处在规划的6个milestone中第3&4个。

低。使用简单，几个command就可以完成到so的编译。

推荐。

Shed Skin

低。最近一年已经没有更新了。

不友好。采用GPL3协议，对使用者知识产权有侵害。

中。有简单的使用文档。

差。在提及到的文档里，只支持2.4-2.7.

无。

低。使用简单。

不推荐。

 

综上：

我个人推荐我们使用Nuitka。使用简单，成本低，目标明确，对python版本兼容好，开发社区活跃，目前虽然还处于项目的中期，但是已发布的版本对于我们的场景足够了。

 


请在原麦项目二期的时候，尝试使用Nuitka来发布我们的产品，目标：用于面包识别的算法代码使用native code来发布，和售卖相关的业务可以继续使用python源码发布，调用算法的地方(可能)需要稍作修改。

 

由于我司目前几乎全部工程都在使用python源码的方式，这个尝试为未来我们的知识产权保护能够探索出一条可实践的道路。
