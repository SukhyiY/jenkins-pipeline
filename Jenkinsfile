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
    
    stage ('Checkout SCM') {
         git credentialsId: 'git-creds', url: 'https://github.com/SukhyiY/jenkins-pipeline'
    }
   
    stage('Set correct tags') {
      if (env.GIT_BRANCH == 'master') {
        env.IMAGE_TAG="${env.GIT_BRANCH}-${env.GIT_COMMIT}"
      }
      else if (env.TAG_NAME) {
        env.IMAGE_TAG="${env.TAG_NAME}"
      }
      else {
        env.IMAGE_TAG="${env.GIT_BRANCH}"
      }
    }
   
    stage ('Build Dockerfile and push image to DockerHub') {
      container('docker') {
        sh """
        docker build --no-cache -t ysukhy/myimage:${env.IMAGE_TAG} .
        docker network create --driver=bridge myimage
        docker run -d --name=myimage --net=myimage ysukhy/myimage:${env.IMAGE_TAG}
        docker run -i --net=myimage appropriate/curl /usr/bin/curl myimage:80
        """
        if (env.CHANGE_ID == null) {
          withCredentials([string(credentialsId: 'docker-pwd', variable: 'dockerhub_pwd')]) {
            sh """
            docker login -u ysukhy -p ${dockerhub_pwd}
            docker push ysukhy/myimage:${env.IMAGE_TAG}
            """
          }
        }
      }
    }
   
  }
}
