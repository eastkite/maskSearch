# id_rsa.pub 을 pubkey 로 지정
MY_KEY=$(cat ~/.ssh/id_rsa)
echo $MY_KEY

docker build --build-arg SSH_KEY="$MY_KEY" -t searchmask:0.1 .
docker run -d -p 8090:8090 -it --name MaskServer searchmaskl:0.1 /bin/bash