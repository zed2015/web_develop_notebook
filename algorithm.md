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

### cos 距离
```
public static double cosineSimilarity(double[] vectorA, double[] vectorB) {
    double dotProduct = 0.0;
    double normA = 0.0;
    double normB = 0.0;
    for (int i = 0; i < vectorA.length; i++) {
        dotProduct += vectorA[i] * vectorB[i];
        normA += Math.pow(vectorA[i], 2);
        normB += Math.pow(vectorB[i], 2);
    }   
    return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
}

```
### 跳表
> `https://cloud.tencent.com/developer/article/1353762`
