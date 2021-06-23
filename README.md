# K8S hands-on drill


## :memo: Where do I start?

### Step 1: Create a cluster with aks-engine
- Edit `aks-engine/cluster.json` and add your SSH public key
- Run aks-engine:
`aks-engine deploy --dns-prefix=<DNS-PREFIX> --resource-group=<RESOURCE-GROUP> --auto-suffix --location=<LOCATION> --api-model=aks-engine/cluster.json`
For example:
`aks-engine deploy --dns-prefix=ravid-test --resource-group=ravidbrown --auto-suffix --location=westus2 --api-model=aks-engine/cluster.json`
- Set KUBECONFIG from _output folder

### Step 2: Install ingress-controller
- Deploy nginx-ingress-controller
`ingress-controller/install-ingress-controller.sh`
- Use `kubectl get service -n ingress-basic` to get the EXTERNAL-IP of the Ingress Controller
- Set FQDN
`ingress-controller/set-dns-ingress-controller.sh <EXTERNAL-IP> <DNS-NAME>`
For example:
`ingress-controller/set-dns-ingress-controller.sh 20.99.176.132 ravid-test-ingress`
The FQDN is printed to the screen
- Install cert manager
`ingress-controller/install-cert-manager.sh`
- Deploy cluster issuer
`kubectl apply -f ingress-controller/cluster_issuer.yaml`

### Step 3: Deploy services
- Deploy service requirements:
`kubectl apply -f k8s-manifests/namespace.yaml`
`kubectl apply -f k8s-manifests/rbac.yaml`
- Deploy services
**Update tls:hosts on ingress resource if needed 
(Default:ravid-test-ingress.westus2.cloudapp.azure.com)**
`kubectl apply -f k8s-manifests/services.yaml`

:rocket: 
**The sources for the bitcoin service can be found under `bitcoin_service` folder**
