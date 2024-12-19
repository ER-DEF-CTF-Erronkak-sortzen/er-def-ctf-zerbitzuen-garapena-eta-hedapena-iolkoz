# Service definition:
- We have three dockers: 
1. An API developed with Flask that contains the flags. 
2. A website with a login page.
3. A database to support the website
The attacker has access to the web (web_docker) and has to look for information that can help him using the API in the other container.
The flags are stored in the API and attacker has to let them in his T-Submission machine. 

# Service implementation:

web docker is configured to take a copy index.html file from the host machine, letting it in '/usr/local/apache2/htdocs/index.html'. 
ssh docker is configured attending to the following tips:
  - It has openssh-server installed and started. 
  - It has a user called 'dev1' whose password is 'w3ar3h4ck3r2'. 

 'dev1' user's password will never be changed. Moreover, if a team changes it, it will be losing SLa points. 
 
-Flags: 
    Flags will be stored in 'toritoken_ssh_1' docker's '/tmp/flags.txt' file. 

# About exploting:
- The attacker has to exploit the login page in the web. It can be done in two ways: bruteforce or SQLinjection.
- With the information gathered in the web, the attacker must craft a request for the API to get the flag.
- The defender should change the web users credentials. This can be done in the mysql container.
- Another option is to secure the login code in the web container.
  
  Attack performed by Team1 against Team 4. 
  Inspect web page
      Brute force the login (weak credentials)
      Exploit the login form using SQLinjection
      So, we get the credentials to  use the API
  Inspect the API, paying attention to the messages
  Using postman or similar, craft a request to the API
      The API returns the flag content
  Paste copied flags. 

  Defense performed by Team4
    Enter the mysql container, then from mysql console, change the passwords
    Enter the web container, in app.py file change the code to use parametrized queries for example
     

# Checker checks:
- Ports to reach dockers are open (WEB:5000; API 5001)
- /app/templates/login.html file's content from toritoken_web docker has not been changed. 
- /app/app.py file's content from toritoken_api docker has not been changed. 
- The web app must have a functional login





