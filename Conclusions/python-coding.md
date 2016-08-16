
### Question

当我在使用 python 做爬虫的时候，由于要涉及到接收网络数据，我发现会因此而引起许多问题，比如：

1. 从网络上接收的数据并不能进行 `str` 的相关操作

2. 将 `str` 的字符作为 `socket.send()` 的参数会产生错误：

    ```shell

    sckt.send(get)

    TypeError: a bytes-like object is required, not 'str'

    ```

3. 当代码文件中含有中文的时候，必须在文件开头加上：`# coding: utf-8`



### Abstract

阅读完本文，你将会明白以下两件事：

1. 几种常见编码格式的含义

2. 使用 python 会遇到的编码问题

### 几种常见的编码格式

#### ASCII

ASCII 是 American Standard Code for Information Interchange 的缩写。



实际上就是英文字符，在计算机的表示中利用一个字节（00～7F）表示的 128 个字符，除了可以输出的字符外，还包括控制字符



### GBK

为了表示汉字，GB2312 被制定了下来，但是由于汉字众多，于是后来又在 GB2312 的基础上发展出 GBK，包括汉字以及少数民族的文字，当然也包括 ASCII 编码，这就意味着有的字符是 1 个字节，有的字符是 2 个字节，如何区分也是 GBK 所规定的，和其他编码不一样。



其中有意思的是，GB 是国家（Guojia Biaozhun）的首字母，K 是扩展（Kuozhan）的首字母。



另外需要指出的是 GBK 是作为 Unicode 的一种具体实现方式



### Unicode

Unicode 是 Unique, Universal, and Uniform character encoding 的缩写。



从名字就可以看出来这是针对全球语言制定的编码，但是需要指出的是虽然名称中带有 encoding，但是实际上与上面提到的两种编码存在一点区别——上面两种不仅将符号编码（encoding）成数字，并且在计算机中也是利用存储这些数字来表达它们的，然而 Unicode 却没有涉及到后者。因此你可以将 Unicode 看成某种 API 的描述，其实现方式存在很多种，更具体地说，Unicode 给世界上每一个字符指定了唯一的数字，但是在计算机中如何表示这样的数字存在着不同的方式，包括 UTF-8，UTF-16，UCS-2 等等。



现在举例来说明，UTF-8 的编码规则可以用下表来说明：







根据表格可以观察出这样一个结论：

**开始字节从高到低若是有 n 个1，那么就说明该字符需要用 n+1 个字节来表示**



那么接下来有两个问题：

1. 给定一个字符，如何利用 UTF-8 来表示？

2. 给定了一串 UTF-8 的字节串，如何正确地识别出每个字符？



_Solution_

1. 给定一个字符，可以根据 Unicode 知道其对应的数据，然后利用上表提供的对应规则来得到表达的 UTF-8 编码

2. 根据表格的观察结果可以知道，从给定的字节串从头开始分析，从第一次开始就可以确定第一个字符需要几个字节来表示，那么之后每次都可以确定几个字节是一个字符。



### 使用 python 会遇到的编码问题

#### python3 与 python2 在编码上的区别

首先必须强调的是，python3 与 python2 对 unicode 的支持有着非常大的变化，以至于在讨论编码的时候必须强调使用的是 python3 还是 python2，其中一个最明显的区别在于 python2 在运行 `.py` 文件的时候，默认采用 ASCII 的格式，所以在多数情况下，如果 `.py` 文件中存在非 ASCII 字符，最好使用

``# -*- coding: utf-8 -*-``

来保证兼容性。



下面谈论的 python 版本将默认是 python3，python3 默认采用 UTF-8 来编码。

#### 概念： encode & decode

实际上，解决 python 中会遇到的问题核心在于理解 encode 与 decode 这两个概念（注意，python 中有 encode 和 decode 这两个函数，本文这里提到是更广泛意义上的概念，而不仅仅是这样两个函数）。



encode：是指使用一个计算机可以理解的数字（code point）来代替人类认识的文字

decode：是 encode 的逆过程，将计算机中存储的数字解码成人类可以认识的文字



无论是 encode 还是 decode 必须指定编码的格式，因此可以观察得出的结论是：

**一切 python 的编码问题都在于 encode 或 decode 时使用了错误的编码格式**



python 中有 encode 和 decode 这两个函数，但它们是不同类的方法，有不少类都含有这个方法，但是值得注意的是：

    1. `str` 类不含有 decode 方法，但含有 encode 方法

    2. `bytes` 类不含有 encode 方法，但含有 decode 方法



这其实是可以理解的，`str` 类的对象是人类可以认识的文字（ python 存储在计算机中的文字实际上也是按照 UTF-8 来编码的），所以可以将其 encode 成某种编码。而 `bytes` 类实际上是以字节作为存储单位，没有其他含义，需要将其 decode 成可以理解的文字。

我在写爬虫的过程中，利用 socket 来接收和发送数据，而 socket 接收和传送的数据必须是     `bytes-like` 的数据格式，因此在发送前必须进行 encode，在接收到数据后，必须进行 decode。





那么接下来的问题就是用什么编码格式来进行 encode 和 decode 呢？

现在 HTML5 已经默认将 UTF-8 作为默认编码，所以一般来说可以使用 UTF-8（实际上，如果不带参数的话，这两个函数都是默认使用 UTF-8）

当然，在做爬虫的时候，不可能所有文件都是 UTF-8 的，比如图片信息，肯定不是 UTF-8，这个时候，可以通过提取 HTTP 的头部信息，利用 Context-type 域的信息来获取编码信息，比如：



    ```html

    Content-Type: text/html; charset=utf-8

    ```



仔细想一下，你可能会发现这样一个问题，为了知道编码格式，必须提取 HTTP 头部信息，但是不知道编码格式，又怎么提取头部信息呢？

其实，接收过来的数据都是字节，而 HTTP 的头部肯定都是 ASCII 格式的数据，所以可以直接按照 ASCII 来提取头部信息，具体是这样的:



    ```python

    def isHtml(self,text):

        header,_ = text.split(b'\r\n\r\n',1)

        header_dict = dict(h.split(b": ",1) for h in header.split(b"\r\n")[1:])

        is_html = header_dict.get(b'Content-type')

        if not is_html:

            return False

        else:

            return is_html.startswith(b'text/html')

    ```

这段代码有几个细节，但是不在这里细述了，唯一要提的就是参数 `text` 是 `bytes` 类，所以在之后使用的方法 split、get、startswith 的参数都是 `bytes` 类型的。



### 参考

1. [ python 官方文档中阐述 python3 对 Unicode 的支持 ](https://docs.python.org/3/howto/unicode.html)

2. [ 知乎回答 -- 注意该答案提到的 python 版本为 2.x ](https://www.zhihu.com/question/31833164/answer/114694586)

