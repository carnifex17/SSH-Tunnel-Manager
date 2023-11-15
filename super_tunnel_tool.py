import json, subprocess,os,time,sys
class Tunnel:
    
    tunnel_config = {}# Initialize an empty dictionary for the tunnel configuration

    def Banner():
        print("\n")
        print("""   __________ __       ______                       __
  / ___/ ___// /_     /_  __/_  ______  ____  ___  / /
  \__ \\\__ \/ __ \     / / / / / / __ \/ __ \/ _ \/ / 
 ___/ /__/ / / / /    / / / /_/ / / / / / / /  __/ /  
/____/____/_/ /_/    /_/  \__,_/_/ /_/_/ /_/\___/_/   
   /  |/  /___ _____  ____ _____ ____  _____          
  / /|_/ / __ `/ __ \/ __ `/ __ `/ _ \/ ___/          
 / /  / / /_/ / / / / /_/ / /_/ /  __/ /              
/_/  /_/\__,_/_/ /_/\__,_/\__, /\___/_/               
                         /____/      
Made by carnifex17""")

    def add_tunnel():#Add new data or just completes the dictionary with tunnel config data 
        tunnel_name = input("Enter Tunnel name: ")
        if tunnel_name in Tunnel.tunnel_config:#Checking existing names
            print(f"Tunnel with the name '{tunnel_name}' already exists.")
            return
        else:  
            tunnel_type = input("Enter Type: ")
            l_port = int(input("Enter L-Port: "))
            ip = input("Enter remote IP: ")
            r_port = int(input("Enter R-Port: "))
            tunnel_username = input("Enter remote username: ")
            Tunnel.tunnel_config[tunnel_name] = {#Adding data to tunnel_config dictionary
                "Type": tunnel_type,
                "L-Port": l_port,
                "IP": ip,
                "R-Port": r_port,
                "User": tunnel_username
            }
            print(Tunnel.tunnel_config)
            if input("Are all the data entered correctly? Y/N: ") == "Y":
                with open("config.json", "w") as json_file:#Making a json file or opening it if existing
                    json.dump(Tunnel.tunnel_config, json_file, indent=4)#Write dictionary data into config
                    print("Writing data")
                    Tunnel.Wait()
            else:
                return

    def exec_tunnel():#Execute existing in config tunnels
        name_tunnel = input("Enter tunnel, which you want to execute: ")
        
        command = [
            "ssh",
            f"-{Tunnel.tunnel_config[name_tunnel]['Type']}",
            f"{Tunnel.tunnel_config[name_tunnel]['L-Port']}:localhost:{Tunnel.tunnel_config[name_tunnel]['R-Port']}",
            f"{Tunnel.tunnel_config[name_tunnel]['User']}@{Tunnel.tunnel_config[name_tunnel]['IP']}"
        ]
        #print(command) Look what command is gonna be executed
        tunnel_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)#Executing process
        print(f"Executing {name_tunnel} tunnel")#Giving effect of working, but at this time process already executed or failed
        Tunnel.Wait()
        if tunnel_process.returncode == 0:
            print("SSH tunnel established successfully")
            print(f"PID of the \'{name_tunnel}\' tunnel process: {tunnel_process.pid}")
        else:
            print("Failed to establish one or both of the SSH tunnels")

    def Show():#Method to show json file
        with open("config.json", "r") as json_file:#Getting dictionary from config if existed
            Tunnel.tunnel_config = json.load(json_file)
        print("Looking for file")
        Tunnel.Wait()
        print(Tunnel.tunnel_config)
        #print(Tunnel.tunnel_config["Tunnel2"]["IP"]) ----- Parse certain data from dic
        
    def Wait():#Method to make waiting effect
        i = 0
        while i < 3:
            print(".", flush = True, end =" ")
            i += 1
            time.sleep(1)
        print("\n")

    def Commands():
        print("""With this tool you could manage address book just with this fancy TUI
Available commands for now is:
Commands
Execute
Clear
Add
Delete
Wait
Show
Banner
""")

#Here's main code begins  
def main():
    Tunnel.Banner()
    if os.path.exists("config.json"):
        with open("config.json", "r") as json_file:#Getting dictionary from config if existed
            Tunnel.tunnel_config = json.load(json_file)
    else:
        print("\nconfig.json does not exist, please make it with Add command\n")
    while True:
        arg=input("> > > ")
        if(arg=="Wait" or arg=="wait"):#Done
            Tunnel.Wait()
        elif(arg=="Change" or arg=="change"):
            Tunnel.Change()
        elif(arg=="Add" or arg=="add"):#Done but not tested
            Tunnel.add_tunnel()
        elif(arg=="Exit" or arg=="exit"):
            exit()
        elif(arg=="Execute" or arg=="execute"):
            Tunnel.exec_tunnel()
        elif(arg=="Banner" or arg=="banner"):
            Tunnel.Banner()
        elif(arg=="Show" or arg=="show"):
            Tunnel.Show()
        elif(arg=="Commands" or arg=="commands"):
            Tunnel.Commands()
        elif(arg=="Clear" or arg=="clear"):
            os.system('clear')
        else:
            print("To watch all possible commands just type \'Commands\'")
    pass

if __name__ == "__main__":
    main()
#Checking if commits working in vscode