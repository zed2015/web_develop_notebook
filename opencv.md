## opencv 读出来的都是bgr
## 人脸模型训练的是rgb的
## affindTransform
> 仿真变换 `https://zhuanlan.zhihu.com/p/23199679`

### transform
> `https://blog.csdn.net/hanshihao1336295654/article/details/83095641`

### 提高摄像头帧率
> 3.4.0 cv2 放在设置图片尺寸之后，4.1.0 放在尺寸设置之前才能生效

```
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
```

