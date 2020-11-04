pwd-$( aws ecr get-login-password)
dicker container stop $(docker container ls -aq)
docker login -u AWS -p $pwd #linkdockerimage
docker pull #link amazon