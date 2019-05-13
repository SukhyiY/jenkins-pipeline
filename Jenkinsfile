node{
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
