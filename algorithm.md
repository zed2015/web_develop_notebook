## 数据结构与算法

### 排序算法
- 冒泡排序
```python3
def buble_sorted(li):
    li_len = len(li)
    for i in range(li_len-1):
        count = 0
        for j in range(li_len-1-i):
            if li[j] > li[j+1]:
                li[j], li[j+1] = li[j+1], li[j]
                count += 1
        if count == 0:
            break
    return li

```

