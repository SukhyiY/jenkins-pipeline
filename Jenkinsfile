node{
    stage ('Checkout SCM'){
        git credentialsId: 'git-creds', url: 'https://github.com/SukhyiY/jenkins-pipeline'}

    stage('Set correct image tag') {
      if (env.GIT_BRANCH == 'master') {
        env.IMAGE_TAG="${env.GIT_BRANCH}-${env.GIT_COMMIT}"}
      else if (env.TAG_NAME) {
        env.IMAGE_TAG="${env.TAG_NAME}"}
      else {
        env.IMAGE_TAG="${env.GIT_BRANCH}"}
    }

    stage ('Build Dockerfile and push image') {
      container('flask-image') {
        sh """
        docker build -t ysukhy/some_image:${env.IMAGE_TAG} .
        docker network create --driver=bridge some_net
        docker run -d --name=some_image --net=some_net ysukhy/some_image:${env.IMAGE_TAG}
        docker run -i --net=some_net appropriate/curl /usr/bin/curl some_image:80
        """
        if (env.CHANGE_ID == null) {
          withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'f74f60fe-bc38-4b3e-ab91-d7af3416231e',
                          usernameVariable: '.....', passwordVariable: '.....']]) 
            {
            sh """
            docker login -u $.... -p $....
            docker push ysukhy/some_image:${env.IMAGE_TAG}
            """
            }
        }
      }
    }
