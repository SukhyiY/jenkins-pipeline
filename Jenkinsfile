def label = "mypod-${UUID.randomUUID().toString()}"

podTemplate(label: 'flask-build', yaml: """
apiVersion: v1
kind: Pod
metadata:
  name: dockerbuild
spec:
  serviceAccountName: nginx-ingress-serviceaccount
  containers:
    - name: helm
      image: alpine/helm
      command:
      - cat
      tty: true
    - name: docker
      image: docker
      command:
      - cat
      tty: true
      # imagePullPolicy: Always
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
){
    
 node ('flask-build') {
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
    def container
    stage ('Build Dockerfile and push image to DockerHub') {
        container = docker.build('some_image:${env.IMAGE_TAG}')
        if (env.CHANGE_ID == null) {
          withCredentials([zip(credentialsId: 'docker-config',
                                    variable: 'DOCKER_CONFIG')]) {
            echo 'Pushing to Docker Hub'
            sh 'docker push ysukhy/some_image:${env.IMAGE_TAG}'
          }
        }
    }
 }
}
