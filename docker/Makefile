# docker user name
NAMESPACE := sarodesparsh

all: authz-docker storage-service-docker language-processor-docker server-docker

server-docker:
	docker build -t $(NAMESPACE)/server -f ./server/Dockerfile ../backend/server/
	docker push $(NAMESPACE)/server

language-processor-docker:
	docker build -t $(NAMESPACE)/language-processor -f ./language-processor/Dockerfile ../backend/llm/
	docker push $(NAMESPACE)/language-processor

authz-docker:
	docker build -t $(NAMESPACE)/authz -f ./authz/Dockerfile ../backend/authz/
	docker push $(NAMESPACE)/authz

storage-service-docker:
	docker build -t $(NAMESPACE)/storage-service -f ./storage-service/Dockerfile ../backend/storage-service/
	docker push $(NAMESPACE)/storage-service

authz-test-docker:
	docker build -t $(NAMESPACE)/test-authz -f ./test-authz/Dockerfile ../backend/authz/
	docker run --rm $(NAMESPACE)/test-authz
	docker rmi $(NAMESPACE)/test-authz

storage-service-test-docker:
	docker build -t $(NAMESPACE)/storage-service-test -f ./storage-service-test/Dockerfile ../backend/storage-service/
	docker run --rm $(NAMESPACE)/storage-service-test

test: authz-test-docker
	

.PHONY: all authz-docker storage-service-docker