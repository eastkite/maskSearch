
#!/bin/bash

# python3 dbCreate.py

if [ -f crawling.pid ]; then
    kill -9 `cat crawling.pid`
fi

if [ -f server.pid ]; then
    kill -9 `cat server.pid`
fi

if [ -f article.pid ]; then
    kill -9 `cat article.pid`
fi

nohup python3 run.py > crawling.out 2>&1 &
echo $! > crawling.pid
nohup python3 ServerRun.py > server.out 2>&1 &
echo $! > server.pid
nohup python3 newArticle.py > article.out 2>&1 &
echo $! > article.pid