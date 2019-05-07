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


