pipeline {
         agent any
         stages {
                 stage('Build') {
                     steps {
                         echo 'Build CredentialDatabase'
                         sh 'pip3 install -r requirements.txt'
                         sh 'python3 setup.py bdist_wheel'
                         sh 'sudo python3 setup.py install'
                     }
                 }
                 stage('Test') {
                    steps {
                        echo 'Test CredentialDatabase'
                        sh 'python3 -m unittest discover CredentialDatabase/test/ -v'
                    }
                 }
                 stage('Deploy') {
                    steps {
                        echo "Deploy CredentialDatabase to target server"
                        sshPublisher(publishers: [sshPublisherDesc(configName: 'christian@server', transfers: [sshTransfer(cleanRemote: false, excludes: '', execCommand: 'sudo pip3 install projects/CredentialDatabase/$BUILD_NUMBER/CredentialDatabase-*.whl', execTimeout: 120000, flatten: false, makeEmptyDirs: false, noDefaultExcludes: false, patternSeparator: '[, ]+', remoteDirectory: 'CredentialDatabase/$BUILD_NUMBER', remoteDirectorySDF: false, removePrefix: 'dist', sourceFiles: 'dist/*.whl')], usePromotionTimestamp: false, useWorkspaceInPromotion: false, verbose: false)])
                    }
                }
    }
}
