## Notes & Writeup for the Friendzonebox

# Checking open ports

Run the following command to check for open ports:

```shell
nmap -A -sC -sV 10.10.10.123
```

This resulted in the following nmap output

```shell
Starting Nmap 7.80 ( https://nmap.org ) at 2020-10-21 01:20 CEST
Nmap scan report for friendzoneportal.red (10.10.10.123)
Host is up (0.023s latency).
Not shown: 993 closed ports
PORT    STATE SERVICE     VERSION
21/tcp  open  ftp         vsftpd 3.0.3
22/tcp  open  ssh         OpenSSH 7.6p1 Ubuntu 4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 a9:68:24:bc:97:1f:1e:54:a5:80:45:e7:4c:d9:aa:a0 (RSA)
|   256 e5:44:01:46:ee:7a:bb:7c:e9:1a:cb:14:99:9e:2b:8e (ECDSA)
|_  256 00:4e:1a:4f:33:e8:a0:de:86:a6:e4:2a:5f:84:61:2b (ED25519)
53/tcp  open  domain      ISC BIND 9.11.3-1ubuntu1.2 (Ubuntu Linux)
| dns-nsid:
|_  bind.version: 9.11.3-1ubuntu1.2-Ubuntu
80/tcp  open  http        Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Friend Zone Escape software
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
443/tcp open  ssl/http    Apache httpd 2.4.29
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Watching you !
| ssl-cert: Subject: commonName=friendzone.red/organizationName=CODERED/stateOrProvinceName=CODERED/countryName=JO
| Not valid before: 2018-10-05T21:02:30
|_Not valid after:  2018-11-04T21:02:30
|_ssl-date: TLS randomness does not represent time
| tls-alpn:
|_  http/1.1
445/tcp open  netbios-ssn Samba smbd 4.7.6-Ubuntu (workgroup: WORKGROUP)
Service Info: Hosts: FRIENDZONE, 127.0.1.1; OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
|_clock-skew: mean: -59m59s, deviation: 1h43m55s, median: 0s
|_nbstat: NetBIOS name: FRIENDZONE, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb-os-discovery:
|   OS: Windows 6.1 (Samba 4.7.6-Ubuntu)
|   Computer name: friendzone
|   NetBIOS computer name: FRIENDZONE\x00
|   Domain name: \x00
|   FQDN: friendzone
|_  System time: 2020-10-21T02:21:02+03:00
| smb-security-mode:
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode:
|   2.02:
|_    Message signing enabled but not required
| smb2-time:
|   date: 2020-10-20T23:21:02
|_  start_date: N/A
```
From this output sevral things can be deducted:

1) Port 21 is open for ftp running [vsftpd 3.0.3](https://en.wikipedia.org/wiki/Vsftpd)
2) Port 22 is open for ssh running [OpenSHH 7.6](https://www.openssh.com/)
3) Port 53 is open for DNS running [BIND 9.11.3](https://nl.wikipedia.org/wiki/BIND)
- BIND is DNS server software so this machine is acting as a DNS server
- This might mean that we could query the zone file of this DNS sever possibly containing addition domains if the DNS server is misconfigured
4) Port 80 is open for HTTP running [Apache httpd 2.4.19](https://nl.wikipedia.org/wiki/Apache_(webserver))
- Apache HTTP is a commonly used webserver, this indicated that a website is running via http on 10.10.10.123 (Hostmachine IP)
5) Port 132 is open for SMB over NetBios running [Samba 3.x-4.x](https://en.wikipedia.org/wiki/Samba_(software))
- Note that port 445 is also open for SMB over NetBios.
6) Port 443 is open for https Running a different version of the Apache webserver
- Http and https connections might lead to different websites
- We also not that the https certificate list a different domain, namely: friendzone.red

# Finding vulnerabilities

First off I wanted to check if ftp allows anonymous login, so I ran the following command:

```shell
ftp 10.10.10.123
```

This however led to unsatifying results as anonymous login was disabled. Next I wanted to know more about the smb application running on port 132. Using the smbmap command:

```shell
smbmap -H 10.10.10.123
````

I was able to get the following output:

```shell
t session       IP: 10.10.10.123:445    Name: friendzoneportal.red                              
        Disk                                                    Permissions     Comment
	        ----                                                    -----------     -------
		        print$                                                  NO ACCESS       Printer Drivers
			        Files                                                   NO ACCESS       FriendZone Samba Server Files /etc/Files
				        general                                                 READ ONLY       FriendZone Samba Server Files
					        Development                                             READ, WRITE     FriendZone Samba Server Files
						        IPC$                                                    NO ACCESS       IPC Service (FriendZone server (Samba, Ubuntu)
```


