def awsCredentials = [[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: '047a2523-0a76-477f-a24d-17efc60b6a82', accessKeyVariable: 'AWS_ACCESS_KEY_ID', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]

pipeline {
    agent { node { label 'prod-nc-slave-01' } }
    options {
        disableConcurrentBuilds()
        withCredentials (awsCredentials)
    }
    environment {
        ENVIRONMENT_NAME = 'cvdemo_5ghacking'
        SERVICE_PATH = ''
        GIT_BRANCH = 'master'
        GIT_REPONAME = 'vision_valley_demo'
        AWS_DEFAULT_REGION = 'eu-west-3'
        AWS_DEFAULT_OUTPUT = 'json'
        CV_VER = '1.0'
    }
    stages {
        stage ('build computer vision NGINX server') {
            steps {
                dir ("${WORKSPACE}/streaming_server/") {
                    sh '''
                         $(aws ecr get-login --no-include-email)
                         docker build . -t 709233559969.dkr.ecr.eu-west-3.amazonaws.com/computer_vision_nginx:${CV_VER}
                       '''
                }
             }
          }
        stage ('push computer vision NGINX to registry') {
            steps {
                dir ("${WORKSPACE}/streaming_server/") {
                    sh '''
                         docker push 709233559969.dkr.ecr.eu-west-3.amazonaws.com/computer_vision_nginx:${CV_VER}
                       '''
               }
             }
        }
    }
    post {
      success {
            echo 'CV NGINX server built and pushed'
            echo ' clean dockerhub credentials'
            sh 'rm -f ${HOME}/.docker/config.json'
      }
    }
  }