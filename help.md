# AWS cloud9 쓸때 docker-compose 다운로드 및 용량 확장

```
다운로드
sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
권한 부여
sudo chmod +x /usr/local/bin/docker-compose
경로 설정
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
버전 확인
docker-compose -v

메모리 확장
wget https://gist.githubusercontent.com/joozero/b48ee68e2174a4f1ead93aaf2b582090/raw/2dda79390a10328df66e5f6162846017c682bef5/resize.sh
두번째 명령
sh resize.sh
여부확인 
df -h

도커사용
1. docker-compose up -d
2. docker ps
3. docker images
4. docker logs (컨테이너 id)
5. docker image rm -f (이미지 id) <- 컨테이너도 동일
6. docker container run -d -p 7777:7777 (이미지명)


주의사항
1. EC2만들어지면 보안그룹에서 포트열기(VPC는 내 드라이브 참고)
2. 경로 잘 확인(컨테이너 환경에서는 그 폴더로 들어와서 수행되는 것.)
```
