# -pyqt-flask
一个用于实时在屏幕上悬空显示多个终端发送的弹幕信息，用户可以通过网页或者微信公众号发送弹幕，桌面实时显示。

项目主要分为两个部分，GUI与服务器。GUI通过qt实现，多个标签从左到右移动。服务器部分可以建立一个简单的flask web应用，可以通过手机或者电脑访问，发送数据；也可以通过微信公众号提供的功能实现。

用了第三方Danmu库，可以直接调用斗鱼的弹幕。
