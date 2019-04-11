## ubuntu k8s集群安装指南

1. 安装docker-ce

	> ./install_docker.sh
	> 
	> apt-cache madison docker-ce 查看可用版本信息
	
	```bash
	sudo apt-get install -y apt-transport-https curl
	
	curl -fsSL http://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
	
	sudo add-apt-repository "deb [arch=amd64] http://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable"
	
	sudo apt-get update
	
	sudo apt-get install docker-ce=18.06.1~ce~3-0~ubuntu
	```

2. 安装k8s前准备
	
	```
	sudo su - 
	echo "deb https://mirrors.aliyun.com/kubernetes/apt/ kubernetes-xenial main" > /etc/apt/sources.list.d/kubernetes.list
	exit
	```

3. 安装kubelet kubeadm kubectl
	
	> ./install_kube.sh
	
	```bash
	sudo swapoff -a
	
	curl -s https://mirrors.aliyun.com/kubernetes/apt/doc/apt-key.gpg | sudo apt-key add -
	
	sudo apt-get update
	
	sudo apt-get install -y kubelet=1.12.3-00 kubeadm=1.12.3-00 kubectl=1.12.3-00
	
	sudo apt-mark hold kubelet kubeadm kubectl
	```
	
	> worker节点需完成以上所有步骤
	> 
	> 还需装k8s.gcr.io/pause:3.1和k8s.gcr.io/kube-proxy:v1.12.3 镜像)

4. 使用kubeadm创建集群

	- 拉取kube依赖镜像脚本 load_images.sh
	
	>  # 查看kubernetes所需镜像
	> 
	> kubeadm config images list --kubernetes-version=v1.12.3
	
	```bash 
	#!/bin/bash
	### config the image map
	declare -A images map=()
	images["k8s.gcr.io/kube-apiserver:v1.12.3"]="registry.cn-hangzhou.aliyuncs.com/google_containers/kube-apiserver:v1.12.3"
	images["k8s.gcr.io/kube-controller-manager:v1.12.3"]="registry.cn-hangzhou.aliyuncs.com/google_containers/kube-controller-manager:v1.12.3"
	images["k8s.gcr.io/kube-scheduler:v1.12.3"]="registry.cn-hangzhou.aliyuncs.com/google_containers/kube-scheduler:v1.12.3"
	images["k8s.gcr.io/kube-proxy:v1.12.3"]="registry.cn-hangzhou.aliyuncs.com/google_containers/kube-proxy:v1.12.3"
	images["k8s.gcr.io/pause:3.1"]="registry.cn-hangzhou.aliyuncs.com/google_containers/pause:3.1"
	images["k8s.gcr.io/etcd:3.2.24"]="registry.cn-hangzhou.aliyuncs.com/google_containers/etcd:3.2.24"
	images["k8s.gcr.io/coredns:1.2.2"]="registry.cn-hangzhou.aliyuncs.com/google_containers/coredns:1.2.2"
	### re-tag foreach
	for key in ${!images[@]}
	do
		docker pull ${images[$key]}				docker tag ${images[$key]} $key			docker rmi ${images[$key]}
	done
	### check
	docker images
	```

5. 初始化集群

	```bash
	sudo kubeadm init --kubernetes-version=v1.12.3 --pod-network-cidr=10.244.0.0/16
	
	## 执行成功可见如下类似输出：
	Your Kubernetes master has initialized successfully!
	
	To start using your cluster, you need to run the following as a regular user:
	
	  mkdir -p $HOME/.kube
	  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
	  sudo chown $(id -u):$(id -g) $HOME/.kube/config
	
	You should now deploy a pod network to the cluster.
	Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
	  https://kubernetes.io/docs/concepts/cluster-administration/addons/
	
	You can now join any number of machines by running the following on each node
	as root:
	
	  kubeadm join 192.168.0.102:6443 --token jpl863.n96ak4a1ph3qnisa --discovery-token-ca-cert-hash sha256:8a0bdb9dde9479e953c460f75628bcfecfd7571b0225496a8a5731be7fe4c555
	
	```

	next：

	```bash
	mkdir -p $HOME/.kube
	sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
	sudo chown $(id -u):$(id -g) $HOME/.kube/config
	```

6. 配置网络插件flannel

	> 配置完等几分钟测试kubectl get nodes，master ready状态

	```bash
	curl -ssL https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml -o kube-flannel.yml
	kubectl apply -f kube-flannel.yml
	```

7. 部署测试kube dashboard

	```bash
	# 拉镜像/改tag/删tag
	docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/kubernetes-dashboard-amd64:v1.6.3
	docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/kubernetes-dashboard-amd64:v1.6.3 gcr.io/google_containers/kubernetes-dashboard-amd64:v1.6.3
	docker rmi registry.cn-hangzhou.aliyuncs.com/google_containers/kubernetes-dashboard-amd64:v1.6.3
	
	# apply dashboard
	curl -ssL https://raw.githubusercontent.com/winse/docker-hadoop/master/kube-deploy/kubeadm/kubernetes-dashboard.yaml -o kubernetes-dashboard.yml
	kubectl apply -f kubernetes-dashboard.yml
	
	# 暴露外网服务(type: ClusterIP修改为type: NodePort)
	kubectl -n kube-system edit service kubernetes-dashboard
	```


### check kube command list

> kubectl get nodes
> 
> kubectl get pod -n kube-system -o wide
> 
> kubectl describe pod podName --namespace=kube-system
>
> kubectl logs -f podName -n kube-system
> 
> kubectl get pods --namespace=kube-system -l k8s-app=kube-dns

### 安装可能遇到的问题issues










