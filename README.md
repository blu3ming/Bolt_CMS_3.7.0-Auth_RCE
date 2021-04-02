# Bolt_CMS_3.7.0-Auth_RCE
Bolt CMS 3.7.0 - Authenticated Remote Code Execution - Enhanced version

+ Original from the user: r3m0t3nu11 (repo)[https://github.com/r3m0t3nu11/Boltcms-Auth-rce-py]
+ Enhanced by: blu3ming

**Usage: python bolt_rce.py username password**

**Note: This script must be executed using Python 2**

![0]

**Main changes**

+ **Use of pwn library for the preogress in every stage of the exploit.**

    ![1]
  
+ **The exploit now doesn't change the users password inside Bolt CMS (to optimize CTF's).**

    ![2]
    
+ **If the exploit could not find a valid session to inject, finishes.**

    ![3]
    
+ **Only prints valid sessions.**

    ![4]
    
+ **Prompt using information of the victim's machine. It remains as a non interactive shell, but looks prettier.**

    ![5]
    
+ **Only prints the result of the command executed, and deletes useless information (from the response, for Python2 users)**

    ![6]
    
+ **Use of the command "exit" to finish the exploit.**

    ![7]
    
+ **CTRL+C defined (it can be used in any moment of the execution).**

    ![8]
    
+ **Deletion of the file "session.txt" when the programm finishes**

    ![9]
    
[0]:./images/0.png
[1]:./images/1.png
[2]:./images/2.png
[3]:./images/3.png
[4]:./images/4.png
[5]:./images/5.png
[6]:./images/6.png
[7]:./images/7.png
[8]:./images/8.png
[9]:./images/9.png
