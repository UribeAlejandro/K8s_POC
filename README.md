# Kubernetes: Proof of Concept

This repository contains a proof of concept of a kubernetes cluster for different projects.

- [Kubernetes: Proof of Concept](#kubernetes-proof-of-concept)
  - [Setup the environment](#setup-the-environment)
    - [Local Cluster Setup](#local-cluster-setup)


## Setup the environment

### Local Cluster Setup

1. Install and configure [Docker](https://docs.docker.com/get-docker/) on your computer.
2. Install [kubectl cli](https://kubernetes.io/docs/reference/kubectl/overview/). In MacOS it can be installed by running

```zsh
    brew install kubectl
```

- **Pro Tip**: you can create a bash alias `alias k="kubectl"` and include it in your `bashrc` file. You are going to be typing `kubectl` quite a lot in your terminal and typing `k` is much more convenient.
- Run the command below to check that the installation completed successfully

```zsh
    kubectl version --client
```

1. Install k3d `kubectl`, which provides a lightweight way to run multi-node Kubernetes clusters in Docker containers. In MacOS it can be installed by running

```zsh
    brew install k3d
```

5. To create a local k3d kubernetes cluster there is a `yaml` [cluster configuration file](cluster/cluster.yaml) included. This configuration file creates:
    - A 3 node cluster (1 master and 2 worker nodes).
    - Binds the ports `8086-8089` from your PC to ports `30086-30089` in the kubernetes cluster master node and ports `8080-8085` from your pc with ports `30080-30085` in the kubernetes cluster worker nodes for networking.
    - Adds some labels to the worker nodes.

For more details on the various options to create a k3d cluster [check this out](https://k3d.io/v5.3.0/usage/configfile/).

To create the cluster applying the configuration run in your terminal the following from the directory containing the [cluster configuration file](cluster/cluster.yaml)

```zsh
k3d cluster create --config cluster.yaml
```

- Note that you need to create a directory in your pc `k3dvol` and mount it to the cluster by replacing the path to the
  directory in the `volumes` section of the cluster configuration file.

6. Run

```zsh
kubectl config use-context k3d-clp
```

and

```zsh
kubectl cluster-info
```

if everything went well you should see information about the newly created cluster, something like

```bash
Kubernetes control plane is running at https://0.0.0.0:51181
CoreDNS is running at https://0.0.0.0:51181/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
Metrics-server is running at https://0.0.0.0:51181/api/v1/namespaces/kube-system/services/https:metrics-server:https/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```

To check the nodes in the cluster run

```zsh
kubectl get nodes
```

and you should see something like

```zsh
NAME               STATUS   ROLES                  AGE   VERSION
k3d-poc-server-0   Ready    control-plane,master   3m41s   v1.27.5+k3s1
k3d-poc-agent-0    Ready    <none>                 3m39s   v1.27.5+k3s1
k3d-poc-agent-1    Ready    <none>                 3m38s   v1.27.5+k3s1
```

to see the labels run

```zsh
kubectl get nodes --show-labels
```

to see all the nodes in the cluster run

```zsh
kubectl get nodes -o wide
```

to see all clusters in your computer run

```zsh
kubectl config get-contexts
```

or

```zsh
k3d cluster list
```

7. To delete the cluster run

```zsh
k3d cluster delete poc
```
