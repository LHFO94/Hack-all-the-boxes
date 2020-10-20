## Notes & Writeup for the Friendzonebox

Run the following command to check for open ports:

```shell
nmap -A -sC -sV 10.10.10.123
```





Several things become clear from this result:

1) Port 21 is open running vsftpd 3.0.3 
2) Port 22 is open running ssh
3) port 53 is open running version 9.11.3 of BIND -> Bind is a DNS 

       
