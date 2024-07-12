# opentel-playground
1. create venv

`python -m venv ./`

2. activate venv (macos/linux)

`source ./bin/activate`

3. install requerements

`pip install -r ./requirements.txt`

4. deploy jaeger to azure kubernetes

`az login`

`az account set --subscription [YOUR SUBSCRIPTION]`

`sudo az aks install-cli`

`az aks get-credentials --resource-group [YOUR RG] --name [YOUR ]`

`kubectl create namespace observability`

`kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.15.1/cert-manager.yaml -n observability`

`kubectl create -f https://github.com/jaegertracing/jaeger-operator/releases/download/v1.57.0/jaeger-operator.yaml -n observability`

`kubectl apply -f simplest.yaml`

`kubectl patch service simplest-collector -p '{"spec": {"type": "LoadBalancer"}}'`

`kubectl patch service simplest-query -p '{"spec": {"type": "LoadBalancer"}}'`

wait a few secs and check the external ip

`kubectl get services `

UI port: 16686
Collector-port: 4318

replace the ip of the collector in pain.py

5. check out the help command

`python main.py -h`

6. run a few examples, like

`python main.py --serviceName=gateway-service --spanName=ingestion`

`python main.py --serviceName=gateway-service --spanName=ingestion --parentTraceId=123`

`python main.py --serviceName=processing --spanName=transformation-abc --tags="LES_ID=12345,BEAN_PELT_ID=9999" --parentTraceId=123`

(refresh the span details page)

`python main.py --serviceName=processing --spanName=transformation-abc --tags="LES_ID=12345,BEAN_PELT_ID=9999" --parentTraceId=123 --startTime=1720780649000000000 --endTime=1720784249000000000` 

(these will likely be way in the past (2024-07-12))


ZZZ. after you're done with the demo, scale to 0 replicas or remove the namespace completely
`kubectl scale --replicas=0 deployment/simplest`
