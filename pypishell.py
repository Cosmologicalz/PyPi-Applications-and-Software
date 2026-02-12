import time, gdown, os, shutil, json
from time import sleep
from ast import literal_eval

ignore = False
version = "1.0.1"
build = "11.2.2026"

try:
    class progbar:
        def progressbarcreate(pre="", length=20):
            print(pre, f"[{("-")*length}] 0%", end="", flush=True, sep="")
            return [pre, length]
            
        def progressbarupdate(bar, value):
            precent = (value/bar[1])*100
            print(bar[0], f"\r[{(("#")*value)+("-"*(bar[1]-value))}] {str(precent)}%", end="", flush=True, sep="")
    
    def firstLaunch(): # Reads the fl.ppsf file to see if this is the first launch
        # open file
        print("Is First Launch... (reading)", end="", flush=True)
        data = 0
        try:
            with open("data/pyapshell/fl.ppsf", "r") as f:
                data = f.read()
            
            # Write a file when the ini starts, incase the user closes it it can detect it and fix it
            if os.path.exists("data/pyapshell/isgoing.ppsf"):
                with open("data/pyapshell/isgoing.ppsf", "r") as f:
                    isGoing = f.read()
                    if isGoing == "True":
                        shutil.rmtree("cache/gdowncache")
                        shutil.rmtree("shl/")
                        with open("data/pyapshell/fl.ppsf.ppsf", "w") as f:
                            f.write("True")
                        with open("data/pyapshell/isgoing.ppsf", "w") as f:
                            f.write("True")
            else:
                with open("data/pyapshell/isgoing.ppsf", "w") as f:
                    f.write("True")
        except Exception as e:
            print("\rIs First Launch... (failed)  ")
            print(e)
            return
        print("\rIs First Launch... (complete)", end="", flush=True)
        
        if data == "True": # if True in the file
            with open("data/pyapshell/fl.ppsf.ppsf", "w") as f:
                f.write("False")
            update()
        else: # if False or nothing or is not True, return since its not the first launch
            os.system('cls')
            return            
            
    def update(isupdate=False):       
        if isupdate:
            print("\nRemoving : shl/def/ [------] 0%", end="", flush=True)
            shutil.rmtree("shl/def/")
            print("\rRemoving : shl/def/ [######] 100%")
        
        print("\nGrabbing folders")
        folders = ["shl/", "shl/def"]
        
        print("Creating folders")
        for i in folders:  # folder creation
            print("\t", f"Creating '{i}'\t\t[-------] 0%", end="", flush=True)
            os.makedirs(i, exist_ok=True)
            print("\r\t", f"Creating : '{i}'\t\t[#######] 100%")
            
        print("Done\n")
        print("Creating Cache...", end="", flush=True)
        os.makedirs("cache/gdowncache", exist_ok=True) # Create a cache for downloads
        print("\rCreating Cache... (complete)")

        print("\nDownloading Files\n\n")
        try:
            gdown.download_folder(id="1PycpA_L2OMDH5OIOU6yfvDcJrxt4srHu", output=f"cache/gdowncache/", quiet=False) # download folders
        except RuntimeError as e:
            print(f"\r\tdownload (Failed) -> {e}\n")
            return
        except Exception as e:
            print(f"\r\tdownload (Failed) -> {e}\n")
            return
        print("Done")
        
        print("\n\nReading Cache")
        moveTo = os.listdir("cache/gdowncache")
        print(moveTo)
        
        print("Installing Files")
        for i in moveTo:
            print(f"\r\tMoving : {i} to {i}\t[----] 0%", end="", flush=True)
            try:
                shutil.move(f"cache/gdowncache/{i}", f"shl/def/{i}")
            except FileExistsError as e:
                continue
            except Exception as e:
                print(f"\r\tMoving : {i} to {i}\t(failed)")
                continue    
            print(f"\r\tMoving : {i} to {i}\t[####] 100%")
        print("Done")
        
        print("\nRemoving cache : cache/gdowncache/ [------] 0%", end="", flush=True)
        shutil.rmtree("cache/gdowncache") # Remove gdowncache
        print("\rRemoving cache : cache/gdowncache/ [######] 100%")
        
        with open("data/pyapshell/isgoing.ppsf", "w") as f:
            f.write("False")        
        
        print("READ: If anyfiles for the shell got corrupted or incorrectly downloaded or anypossible defect/problem you find with the update. Type 'FORCE UPDATE' to update the system.")
        print("Update Complete (clearing in 10 seconds)")
        sleep(10)
        os.system('cls')
    
    firstLaunch()
    
    print(f"[version {version} | build {build}]\nPyPi Applications and Software\n")
    
    while True:
        global lines, whole
        request = input("-> ") # Requesnt a command
        
        if request == "":
            continue
        if request == "FORCE UPDATE":
            update()
        
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