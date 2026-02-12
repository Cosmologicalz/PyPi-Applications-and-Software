import time, gdown, os, shutil, json
from time import sleep
from ast import literal_eval

ignore = False
version = "1.0.1"
build = "11.2.2026"

try:
    print(f"[version {version} | build {build}]\nPyPi Applications and Software\n")
    
    while True:
        global lines, whole
        request = input("-> ") # Requesnt a command
        
        if request == "":
            continue
        
        try:
            with open("shl/def/commands.json", "r") as f:
                data = json.load(f)
             
            if request not in data:
                raise KeyError("Command not found") 
                
            commandData = data[request]
            commandFile = commandData[0]
            
            with open(commandFile, "r") as f: 
                lines = f.readlines()
                
        except Exception as e:
            print("command not recognized")         
            continue
            
                
        # parsing and execution
        try:
            for line in lines:
                line = line.strip()
                
                # Wether the file is all python or pps-c
                if line.startswith("@nonexecutable"):
                    continue
                    
                if ignore:
                    ignore = False
                    continue
                    
                if line.startswith("@ignore"):
                    ignore = True
                    continue

                # Print command
                if line.startswith("@say "):
                    print(line.replace("@say ", "", 1).strip())
                
                # Function handling
                if line.startswith("@function "):
                    # remove prefix
                    func_line = line.replace("@function ", "", 1).strip()
                    # split into Request ./ function
                    bef, sep, aft = func_line.partition("./")
                    bef = bef.strip()
                    aft = aft.strip()
                    
                    # only execute if request matches the before
                    if bef == request:
                        
                        if "~~~" in aft:  # Python code, ~~~ is used to execute functions within this file
                            # remove marker
                            code = aft.replace("~~~", "").strip()
                            try:
                                exec(code)  # run Python code
                            except Exception as e:
                                print(f"Error executing {code}: {e}")
                        
                        else:
                            if aft.startswith("@say "):
                                print(aft.replace("@say ", "", 1).strip())
                                
                            
                    

                
                    
                    
                    
                    
                    
                    
                    
                    
        except Exception as e:
            print(f"Exception : {e}")         
            continue

 
except FileNotFoundError as e:
    os.system('cls')
    print("File Not Found")
    print(e)
    input()
except Exception as e:
    os.system('cls')
    print("Exception")
    print(e)
    input()