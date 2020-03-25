# 网络实验班大作业 - 健康检测平台

管理武汉肺炎期间用户信息，运动轨迹，身体情况

1. 前端是http（https）的网络，外加html或者json网页

Http：超文本传输协议（HyperText Transfer Protocol)是互联网上应用最为广泛的一种网络协议。提供了一种发布和接收HTML页面的方法。

Https：是以安全为目标的Http通道，是Http的安全版。
[免费证书生成](https://www.cnblogs.com/osfipin/p/freessl.html) 

HTML：超文本标记语言，告诉浏览器如何构建网页
([codepen.io](https://codepen.io) HTML CSS JS开发平台，可以实时演示网站效果)

2. 后端是MySQL数据库

MySQL所使用的 SQL 语言是用于访问数据库的最常用标准化语言。

[一个关于HTTP HTML CSS MySQL等等的语法综合教程](https://www.runoob.com/http/http-tutorial.html)

3. 数据采集可能用到chrome wx的gps等等
位置信息：
	1. 车站检查，医院等级（系统输入）
	2. 利用浏览器和微信获取位置

		[html5 geolocation in Chrome](https://developer.mozilla.org/en-US/docs/Web/API/Geolocation_API)

		[微信小程序获取位置信息](https://www.jianshu.com/p/e232c3c9af37)



4. 以太坊Go语言[开发平台](https://geth.ethereum.org)


# 武汉开源项目

[汇总1](https://weileizeng.github.io/OpenSourceWuhan/)

[汇总2](https://github.com/JackieZheng/2019-nCoV)

其他样例：[学生成绩管理系统](https://github.com/86XIng/-Student-Achievement-Management-System)


# 功能
1. 采集用户位置信息（浏览器，微信，车站数据），存储在数据库中
2. 网页内容：
	1. 根据数据库的用户信息，实时在地图上标记各用户的位置（即每当位置改变，就在网页上更新位置），并按照确诊/疑似/普通采用不同记号；
	2. 显示当前擅自移动的用户名单；
	3. 显示隔离用户最新位置对应的以太坊区块
	4. 隔离用户（确诊/疑似）未经允许行动时，在网站上进行标记
3. 在以太坊上维护隔离用户的当前位置

# 分工
* 前端：
  * [疫情地图1](https://github.com/guanyilun/wuhan_viz/blob/master/js/china.js)：自动提取丁香园的数据，并以网页的形式绘制疫情地图。我们数据提取（.json）可以参考这个。
  * [疫情地图2](https://github.com/hack-fang/nCov) 同上
* 后端 + 数据采集 + 数据库
* 区块链 以太坊

# 更新

[flask教程（包括安装）](https://www.bilibili.com/video/BV17W41177oE?p=10) 

[mysql入门](https://blog.csdn.net/hzw6991/article/details/87893761) （教程里不包括安装，可以去官网自己装）

python3+mysql+flask 实现登陆，参考的[这篇](https://blog.csdn.net/weixin_34248118/article/details/88912410?depth_1-utm_source=distribute.pc_relevant.none-task&utm_source=distribute.pc_relevant.none-task)

python3+mysql+flask 实现增删改查，参考的[这篇](https://blog.csdn.net/weixin_34288121/article/details/85959861?depth_1-utm_source=distribute.pc_relevant.none-task&utm_source=distribute.pc_relevant.none-task)


