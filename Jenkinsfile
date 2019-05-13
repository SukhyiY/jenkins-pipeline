node{
    stage ('Checkout SCM'){
        git credentialsId: 'git-creds', url: 'https://github.com/SukhyiY/jenkins-pipeline'
    }
    stage('Set correct tags'){
      if (env.GIT_BRANCH == 'master'){
        env.IMAGE_TAG="${env.GIT_BRANCH}-${env.GIT_COMMIT}"
      }
      else if (env.TAG_NAME){
        env.IMAGE_TAG="${env.TAG_NAME}"
      }
      else{
        env.IMAGE_TAG="${env.GIT_BRANCH}"
      }
    }
    stage ('Build Dockerfile and push image to DockerHub'){
      container('flask-image'){
        sh 'docker build -t ysukhy/some_image:${env.IMAGE_TAG} .'
        sh 'docker network create --driver=bridge mynetwork'
        sh 'docker run -d --name=some_image --net=mynetwork ysukhy/some_image:${env.IMAGE_TAG}'
        sh 'docker run -i --net=mynetwork appropriate/curl /usr/bin/curl some_image:80'
        if (env.CHANGE_ID == null){
          withCredentials([zip(credentialsId: 'docker-config',
                                    variable: 'DOCKER_CONFIG')]) {
            echo 'Pushing to Docker Hub'
            sh 'docker push ysukhy/some_image:${env.IMAGE_TAG}'
          }
        }
      }
    }
}
