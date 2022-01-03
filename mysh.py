#!/usr/bin/env python

# the first line is for the user want to use the project without de need to write (python etc...) 

import os
import sys
import subprocess

# I define here 4 variables, which will be useful in my code
listes=[]
listespath=[]
result=""
c=True

# So this is the function which realize the user's entry (command) 
def commande(code):

    # I define here 4 variables, which will be useful to us (when we want to use another command these variables will be reset)
    listes=[]
    listespath=[]
    result=""
    c=True
    # Here I define two case, espcially for redirections and "sh" command
    
    # Let's imagine that we have the case of cat text.txt>text2.txt so without a space so we need to add a space 
    if ">" in code:
        listes2=[]
        listes.extend(code.split(">"))
        listes.extend(" ")
        listes[len(listes)-1]=listes[len(listes)-2]
        listes[len(listes)-2]=">"
        for i in range(0,len(listes)):
            listes2.extend(listes[i].split(" "))
        if '' in listes2:
            listes2.remove('')
        listes=listes2
    # Like the first case, if we have a .sh or the commande line begin with sh, we need to be careful with that

    elif ".sh" in code or (code.startswith("sh ") and ".sh" in code):
        listes.extend(code.split(" "))
        str_match = [s for s in listes if s.__contains__(".sh")]
        s=str_match[0]
        s = ''.join( x for x in s if x not in '"')
    else:
        listes.extend(code.split(" "))
    while '' in listes:
        del listes[listes.index('')]
    command=listes[0]
    for i in range(1,len(listes)):
        result+=listes[i]
           
    #We catch the PATH of all command in our path and we stock this variable
    path=os.environ["PATH"]
    listespath.extend(path.split(":"))
            
    #In a simple case, I want to find in the all path, if the command exist
    for i in range(0,len(listespath)-1):
        fichier=""
        fichier=listespath[i]+'/'+command
        for i in range(0,len(listes)):
            while os.path.exists(fichier)==True:
                command+=" "+listes[i]
                break
        if os.path.exists(fichier)==True:
            break
            
    #This is the important part of my code, with subprocess.Popen I can use and run the command
    try:
        out = 1
        err = 2

        #But We need to create several if in the case we have some redirections and in this case I remove the redirections and change the stdout or stderr.
        # In this several If,the 'flux' need to be change between out and err  
        if "2>&1" in listes:
            err = 1
            listes.remove("2>&1")
                     
        if ">&2" in listes:
            out = 2
            listes.remove(">&2")

        if "1>&2" in listes:
            out = 2
            listes.remove("1>&2")

        if ">" in listes:
            pos = listes.index(">")
            out = open(listes[pos+1], "wb")
            listes.remove(listes[pos+1])
            listes.remove(">")
                    

        if "1>" in listes:
            pos = listes.index("1>")
            out = open(listes[pos+1], "wb")
            listes.remove(listes[pos+1])
            listes.remove("1>")


        if "2>" in listes:
            pos = listes.index("2>")
            err = open(listes[pos+1], "wb")
            listes.remove(listes[pos+1])
            listes.remove("2>")
            
        #So after that I can use subprocess.Popen and communicate() to launch our shell !!
        process = subprocess.Popen([fichier, *listes[1:]],
                stdout=out, 
                stderr=err,
                stdin=0)
        process.communicate()
        
        # In the case where we have an error I return a message
    except:
        err = "An error has occurred\n"
        print(err, file=sys.stderr)


#region Batch Mode               
arg=sys.argv
fileBatchMode=False
NameOfFile=""
for i in arg:
    if os.path.isfile(str(i))==True and i!=arg[0]:
        fileBatchMode=True
        NameOfFile=str(i)
        break
if fileBatchMode:
    file=open(NameOfFile,"r")
    for line in file.readlines():
        if "exit" not in line.rstrip() and line.strip()!='':
            commande(line.rstrip())
        if "exit" == line.rstrip():
            c=False
    file.close()
#endregion



#region main 
#Otherwise, if we don't need the batch mode or after the batch mode
while c:
    #In this part, I try to test 2 command like local and exit (to stop the program)
    code = input("mysh$ ")
    if code=='exit' or (code.startswith("cd ") or code == "cd"):
            if code =='exit':
                c=False
            elif code.strip() == "cd":
                os.chdir(os.environ["HOME"])
            else:
                try:
                    if len(code.split(" "))==2:
                        os.chdir(code.split(" ")[1])
                    else:
                        newcode=''
                        h=code.split(" ")
                        for i in range(1,len(h)):
                            if i < len(h)-1:
                                newcode+=h[i]+" "
                            else:
                                newcode+=h[i]
                        os.chdir(newcode)
                except:
                    print("Unexpected error:", sys.exc_info()[1])
    #In this part, I recover the user's command and I split it. Then, I find in my computer the list of path where we can find the commands, then to finish (In the case of I don't respect the following if) I take back the command and/or the file        
    #In the others cases
    elif code.isspace()!=True and len(code)>=1:
        commande(code)
#endregion
                        
            