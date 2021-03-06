def label = "mypod-${UUID.randomUUID().toString()}"

podTemplate(label: 'flask-build', yaml: """
apiVersion: v1
kind: Pod
metadata:
  name: dockerbuild
spec:
  serviceAccountName: jenkins
  containers:
    - name: helm
      image: alpine/helm:2.13.1
      command:
      - cat
      tty: true
    - name: docker
      image: docker
      command:
      - cat
      tty: true
      env:
      - name: POD_IP
        valueFrom:
          fieldRef:
            fieldPath: status.podIP
      - name: DOCKER_HOST
        value: tcp://localhost:2375
    - name: dind
      image: docker:18.05-dind
      securityContext:
        privileged: true
      volumeMounts:
        - name: dind-storage
          mountPath: /var/lib/docker
  volumes:
    - name: dind-storage
      emptyDir: {}
"""
) {
    
  node('flask-build') {
    checkout(scm).each { k,v -> env.setProperty(k, v) }
    
    stage('Set correct tags') {
      if (env.GIT_BRANCH == 'master') {
        env.IMAGE_TAG="${env.GIT_COMMIT}"
      }
      else if (env.TAG_NAME) {
        env.IMAGE_TAG="${env.TAG_NAME}"
      }
      else {
        env.IMAGE_TAG="${env.GIT_BRANCH}"
      }
    }
   
    stage ('Build Dockerfile of flask-app') {
      container('docker') {
        sh "docker build --no-cache -t ysukhy/myimage:${env.IMAGE_TAG} ."
      }
    }
    
    stage ('Test connection') {
      container ('docker') {
        sh """
        docker network create --driver=bridge myimage
        docker run -d --name=myimage -e app_version="${env.IMAGE_TAG}" --net=myimage ysukhy/myimage:${env.IMAGE_TAG}
        """
        
        def pair = [:]
        pair["test_connection"] = {
          def connection = sh(script: "docker run -i --net=myimage appropriate/curl /usr/bin/curl myimage:80", returnStatus: true)
            if (connection == 0) {
              echo "Connection SUCCESS"
            }
            else {
              error "Connection FAILED"
            }
        }
        pair["test_output"] = { 
          def output = sh(script: "docker run -i --net=myimage appropriate/curl /usr/bin/curl myimage:80", returnStdout: true)
            if (output.contains("${env.IMAGE_TAG}")) {
              echo "CURL SUCCESS!" 
            }
            else {
              error "CURL FAILED" 
            }
        }
        parallel pair
      }  
    }
    
    stage ('Push image to DockerHub') {
      container ('docker') {    
        if (env.CHANGE_ID == null) {
          withCredentials([string(credentialsId: 'docker-pwd', variable: 'dockerhub_pwd')]) {
            sh "docker login -u ysukhy -p ${dockerhub_pwd}"
            sh "docker push ysukhy/myimage:${env.IMAGE_TAG}"
          }
        }
      }
    }
   
    stage ('Deploy Helm chart') {
      if (env.GIT_BRANCH == 'master' || env.TAG_NAME) {
        container('helm') {
          withCredentials([file(credentialsId: '2conf', variable: 'all_in_one')]) {
              sh "cp ${all_in_one} ./kubeconfig"
              sh "helm init --client-only"
              sh "helm upgrade first-release ./webapp --set image.tag=${env.IMAGE_TAG} --install --wait --timeout 100 --kubeconfig ./kubeconfig"
          }
        }
      }
    }
  }
}
