#!/bin/sh

ID_RSA=~/.ssh/id_rsa.pub 

#  id_rsa.pub 파일이 없을때만 ssh-keygen을 수행합니다.
if [ ! -f $ID_RSA ]; then       
expect -c "spawn ssh-keygen" \
                   -c "expect -re \":\"" \
                   -c "send \"\r\"" \
                   -c "expect -re \":\"" \
                   -c "send \"\r\"" \
                   -c "expect -re \":\"" \
                   -c "send \"\r\"" \
                   -c "puts \" \n * ssh-keygen success!!#3 *\"" \
                   -c "interact"
fi

echo cat ~/.ssh/id_rsa.pub
