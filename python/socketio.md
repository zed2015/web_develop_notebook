### socketio 切换流程
> `https://juejin.im/post/5cc290ee5188252dda0c1117`

### socketio 使用 eventlet、gevent
- socketio 底层建立在engine.io 基础之上
- engine.io 会选择采用long pooling 与 websocket 模式
- 如果是 eventlet 与gevent, 必须在协程里emit 事件，eventlet与gevent的queue，不支持线程模式

