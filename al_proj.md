## 安装 显卡驱动 - `sudo apt install nvidia-384`
- 查看显卡 `lspci|grep VGA`, `lspci|grep -invidia`

## failed call to cuInit: CUDA_ERROR_UNKNOWN
> 正在使用cuda程序，挂起唤醒后，cuda报错，需要关掉程序 `sudo rmmod nvidia_uvm`

```
sudo rmmod nvidia_uvm nvidia_drm nvidia_modeset nvidia
sudo modprobe nvidia_uvm nvidia_drm nvidia_modeset nvidia
```
- export CUDA_CACHE_PATH=/tmp/nvidia
- sudo apt install nvidia-modprobe
### 安装cuda
> https://blog.csdn.net/kaixinjiuxing666/article/details/80321124
- `conda install cudatoolkit=10.0`
### 安装 nvidia-dirver, ppa
> `https://zhuanlan.zhihu.com/p/68069328`

### 安装nvidia-docker
> `https://github.com/NVIDIA/nvidia-docker` docker >=19.03
### anchor 理解
> `https://zhuanlan.zhihu.com/p/63024247`

### retinface fpn:
> `https://blog.csdn.net/wzjwj/article/details/94456036`

### 支持向量机
> `https://tangshusen.me/2018/10/27/SVM/`
