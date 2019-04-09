## 安装 显卡驱动 - `sudo apt install nvidia-384`
- 查看显卡 `lspci|grep VGA`, `lspci|grep -invidia`

## failed call to cuInit: CUDA_ERROR_UNKNOWN

```
sudo rmmod nvidia_uvm
#sudo rmmod nvidia
sudo modprobe nvidia
sudo modprobe nvidia_uvm
```
- export CUDA_CACHE_PATH=/tmp/nvidia
- sudo apt install nvidia-modprobe


