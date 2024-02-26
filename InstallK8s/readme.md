# Install K8s in CentOS 7.9 Minimal

## 环境初始化

```bash
# 所有节点关闭SELinux
SELinux setenforce 0 
sed -i --follow-symlinks 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/sysconfig/selinux

# 关闭swap
swapoff -a
#  注释掉/etc/fsta文件中swap那行
sed -i '/swap/s/^/#/' /etc/fstab
# 添加 Docker 源
yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

# 所有节点关闭firewalld/iptables
systemctl stop firewalld 
systelctl disable firewalld
# yum remove iptables

# 重启之后开始安装K8s
reboot
```

## 服务安装

```bash
# 安装kubelet服务
yum install -y kubelet-1.22.4 kubectl-1.22.4 kubeadm-1.22.4 docker-ce-20.10.24

# 启动服务
systemctl enable kubelet
systemctl start kubelet
systemctl enable docker
systemctl start docker

# kubernetes 官方推荐 docker 等使用 systemd 作为 cgroupdriver
# 否则影响kubelet服务
cat /etc/docker/daemon.json
{   
		"exec-opts": ["native.cgroupdriver=systemd"]
}

# 集群初始化  必须要指定子网
kubeadm init --image-repository=registry.aliyuncs.com/google_containers --pod-network-cidr=10.244.0.0/16 kubernetes-version v1.22.4

# 记录master集群token
# kubeadm token create --print-join-command
kubeadm join 10.0.8.15:6443 --token 73jicr.ch5n5ozvre065rhi \
        --discovery-token-ca-cert-hash sha256:5afd5e97385d07be8b2879fa240666dcdd874610f96f39825e1b8e708195c379

# 如果你其他节点需要访问集群，需要从主节点复制这个文件过去其他节点
mkdir -p $HOME/.kube 
cp -i /etc/kubernetes/admin.conf $HOME/.kube/config 
chown $(id -u):$(id -g) $HOME/.kube/config

# 创建cni网络 详见yaml文件
# kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
kubectl apply -f kube-flannel.yml

# 查看pod创建状态
kubectl get pods -n kube-system

# 集群重置
kubeadm reset

# 查看集群所需镜像信息
kubeadm config images list
```

## yaml文件

```yaml
# cat kube-flannel.yml
# kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
---
kind: Namespace
apiVersion: v1
metadata:
  name: kube-flannel
  labels:
    k8s-app: flannel
    pod-security.kubernetes.io/enforce: privileged
---
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  labels:
    k8s-app: flannel
  name: flannel
rules:
- apiGroups:
  - ""
  resources:
  - pods
  verbs:
  - get
- apiGroups:
  - ""
  resources:
  - nodes
  verbs:
  - get
  - list
  - watch
- apiGroups:
  - ""
  resources:
  - nodes/status
  verbs:
  - patch
- apiGroups:
  - networking.k8s.io
  resources:
  - clustercidrs
  verbs:
  - list
  - watch
---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  labels:
    k8s-app: flannel
  name: flannel
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: flannel
subjects:
- kind: ServiceAccount
  name: flannel
  namespace: kube-flannel
---
apiVersion: v1
kind: ServiceAccount
metadata:
  labels:
    k8s-app: flannel
  name: flannel
  namespace: kube-flannel
---
kind: ConfigMap
apiVersion: v1
metadata:
  name: kube-flannel-cfg
  namespace: kube-flannel
  labels:
    tier: node
    k8s-app: flannel
    app: flannel
data:
  cni-conf.json: |
    {
      "name": "cbr0",
      "cniVersion": "0.3.1",
      "plugins": [
        {
          "type": "flannel",
          "delegate": {
            "hairpinMode": true,
            "isDefaultGateway": true
          }
        },
        {
          "type": "portmap",
          "capabilities": {
            "portMappings": true
          }
        }
      ]
    }
  net-conf.json: |
    {
      "Network": "10.244.0.0/16",
      "Backend": {
        "Type": "vxlan"
      }
    }
---
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: kube-flannel-ds
  namespace: kube-flannel
  labels:
    tier: node
    app: flannel
    k8s-app: flannel
spec:
  selector:
    matchLabels:
      app: flannel
  template:
    metadata:
      labels:
        tier: node
        app: flannel
    spec:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: kubernetes.io/os
                operator: In
                values:
                - linux
      hostNetwork: true
      priorityClassName: system-node-critical
      tolerations:
      - operator: Exists
        effect: NoSchedule
      serviceAccountName: flannel
      initContainers:
      - name: install-cni-plugin
        image: docker.io/flannel/flannel-cni-plugin:v1.4.0-flannel1
        command:
        - cp
        args:
        - -f
        - /flannel
        - /opt/cni/bin/flannel
        volumeMounts:
        - name: cni-plugin
          mountPath: /opt/cni/bin
      - name: install-cni
        image: docker.io/flannel/flannel:v0.24.2
        command:
        - cp
        args:
        - -f
        - /etc/kube-flannel/cni-conf.json
        - /etc/cni/net.d/10-flannel.conflist
        volumeMounts:
        - name: cni
          mountPath: /etc/cni/net.d
        - name: flannel-cfg
          mountPath: /etc/kube-flannel/
      containers:
      - name: kube-flannel
        image: docker.io/flannel/flannel:v0.24.2
        command:
        - /opt/bin/flanneld
        args:
        - --ip-masq
        - --kube-subnet-mgr
        resources:
          requests:
            cpu: "100m"
            memory: "50Mi"
        securityContext:
          privileged: false
          capabilities:
            add: ["NET_ADMIN", "NET_RAW"]
        env:
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        - name: EVENT_QUEUE_DEPTH
          value: "5000"
        volumeMounts:
        - name: run
          mountPath: /run/flannel
        - name: flannel-cfg
          mountPath: /etc/kube-flannel/
        - name: xtables-lock
          mountPath: /run/xtables.lock
      volumes:
      - name: run
        hostPath:
          path: /run/flannel
      - name: cni-plugin
        hostPath:
          path: /opt/cni/bin
      - name: cni
        hostPath:
          path: /etc/cni/net.d
      - name: flannel-cfg
        configMap:
          name: kube-flannel-cfg
      - name: xtables-lock
        hostPath:
          path: /run/xtables.lock
          type: FileOrCreate
```

## 一键安装脚本—maste

```bash
### install master

#!/bin/bash
# verify user
if [ `id -u` -eq 0 ];then
    echo -e "Current User Is Root. Start Install."
else
    echo -e "Current User Is Not Root. Exit..."
    exit
fi

# define hosts
hostname=`hostname|head -n 1`
ipaddr=`ip -4 addr show ens33|grep -oP '(?<=inet\s)\d+(\.\d+){3}'`
# avoid dumplicates
sed -i "/${hostname}/s/^/#/" /etc/hosts
# add hosts
echo "${ipaddr} ${hostname}" >> /etc/hosts

# Verify Versions
kenel=`uname -r`
vers=`cat /etc/centos-release`
if [[ ${kenel}=~"3.10.0-1160.el7.x86_64" ]] && [[ ${vers}=~"CentOS Linux release 7.9.2009 (Core)" ]];then
    echo -e "Verify Kenel and OS Successfully. Start Install."
else
    echo -e "Verify Kenel and OS Version Error. Exit..."
    exit 1
fi

# close firewalld and swap
echo 'start init env...'
systemctl stop firewalld
systemctl disable firewalld
swapoff -a
sed -i '/swap/s/^/#/' /etc/fstab

# remove package
yum remove -y kubelet kubectl kubeadm docker-ce

# unzip files and install packages
tar -zxvf ./resources.tgz
yum install -y ./resources/rpms/*.rpm

yum install -y ./resources/rpms/ansible/*.rpm
ansible --version    
if [ $? -eq 0 ];then
    echo "Install Ansible Successfully"
    sed -i "s/#host_key_checking/host_key_checking/" /etc/ansible/ansible.cfg
    ansible -i K8sConfig all -m ping
    ansible -i K8sConfig node -m copy -a "src=./resources.tgz dest=/data/"
    ansible -i K8sConfig node -m script -a "./resources/scripts/InstallNode.sh"
else
    echo "Install Ansible Error, Exit..."
    exit 0
fi

systemctl enable kubelet
systemctl start kubelet
systemctl enable docker
systemctl start docker

# load images
docker load -i ./resources/images/registry.aliyuncs.com/google_containers/coredns:v1.8.4.tar
docker load -i ./resources/images/registry.aliyuncs.com/google_containers/etcd:3.5.0-0.tar
docker load -i ./resources/images/registry.aliyuncs.com/google_containers/flannel-cni-plugin.tar
docker load -i ./resources/images/registry.aliyuncs.com/google_containers/flannel.tar
docker load -i ./resources/images/registry.aliyuncs.com/google_containers/kube-apiserver:v1.22.4.tar
docker load -i ./resources/images/registry.aliyuncs.com/google_containers/kube-controller-manager:v1.22.4.tar
docker load -i ./resources/images/registry.aliyuncs.com/google_containers/kube-proxy:v1.22.4.tar
docker load -i ./resources/images/registry.aliyuncs.com/google_containers/kube-scheduler:v1.22.4.tar
docker load -i ./resources/images/registry.aliyuncs.com/google_containers/pause:3.5.tar

# define cgroupdriver and reload daemon
echo '{"exec-opts": ["native.cgroupdriver=systemd"]}' > /etc/docker/daemon.json
systemctl daemon-reload
systemctl restart docker.service

# init k8s cluster
kubeadm init --image-repository=registry.aliyuncs.com/google_containers --pod-network-cidr=10.244.0.0/16

kubectl apply -f ./resources/yaml/kube-flannel.yaml

mkdir -p $HOME/.kube
cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
chown $(id -u):$(id -g) $HOME/.kube/config

ansible -i K8sConfig node -m shell -a "mkdir -p /root/.kube"
ansible -i K8sConfig node -m copy -a "src=/root/.kube/config dest=/root/.kube/config"
ansible -i K8sConfig node -m shell -a "chown root:root /root/.kube/config"

joincmd=`kubeadm token create --print-join-command`

ansible -i K8sConfig node -m shell -a "${joincmd}"

echo 'Maste init succsessed.'
echo 'please wait for pods running'
```

```yaml
### 一键安装脚本--node
#!/bin/bash
mkdir -p /data/

# Verify Versions
kenel=`uname -r`
vers=`cat /etc/centos-release`
if [[ ${kenel}=~"3.10.0-1160.el7.x86_64" ]] && [[ ${vers}=~"CentOS Linux release 7.9.2009 (Core)" ]];then
    echo -e "Verify Kenel and OS Successfully. Start Install."
else
    echo -e "Verify Kenel and OS Version Error. Exit..."
    exit 1
fi

# remove package
yum remove -y kubelet kubectl kubeadm docker-ce docker

# unzip files and install packages
tar -zxvf /data/resources.tgz -C /data/

yum install -y /data/resources/rpms/*.rpm > /dev/null

systemctl enable kubelet
systemctl start kubelet
systemctl enable docker
systemctl start docker

# edit /etc/hosts
hostname=`hostname|head -n 1`
ipaddr=`ip -4 addr show ens33|grep -oP '(?<=inet\s)\d+(\.\d+){3}'`
# avoid dumplicates
sed -i "/${hostname}/s/^/#/" /etc/hosts
# add hosts
echo "${ipaddr} ${hostname}" >> /etc/hosts

# load images
docker load -i /data/resources/images/registry.aliyuncs.com/google_containers/coredns:v1.8.4.tar > /dev/null 
docker load -i /data/resources/images/registry.aliyuncs.com/google_containers/etcd:3.5.0-0.tar > /dev/null     
docker load -i /data/resources/images/registry.aliyuncs.com/google_containers/flannel-cni-plugin.tar > /dev/null
docker load -i /data/resources/images/registry.aliyuncs.com/google_containers/flannel.tar > /dev/null
docker load -i /data/resources/images/registry.aliyuncs.com/google_containers/kube-apiserver:v1.22.4.tar > /dev/null
docker load -i /data/resources/images/registry.aliyuncs.com/google_containers/kube-controller-manager:v1.22.4.tar > /dev/null 
docker load -i /data/resources/images/registry.aliyuncs.com/google_containers/kube-proxy:v1.22.4.tar > /dev/null
docker load -i /data/resources/images/registry.aliyuncs.com/google_containers/kube-scheduler:v1.22.4.tar > /dev/null
docker load -i /data/resources/images/registry.aliyuncs.com/google_containers/pause:3.5.tar > /dev/null                   

# define cgroupdriver and reload daemon
echo '{"exec-opts": ["native.cgroupdriver=systemd"]}' > /etc/docker/daemon.json
systemctl daemon-reload
systemctl restart docker.service

kubectl apply -f /data/resources/yaml/kube-flannel.yaml

echo 'node init succsessed.'
echo 'please wait for pods running'
```

```yaml
# config
[all:vars]
ansible_ssh_user=root
ansible_ssh_port=22
ansible_ssh_pass=sysadmin

[master]
10.0.0.100

[node]
10.0.0.101
10.0.0.102
```
