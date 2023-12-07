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
            pid = 0
            ssh_key = input("Enter ssh key name: ")
            tunnel_type = input("Enter Type: ")
            l_port = int(input("Enter L-Port: "))
            ip = input("Enter remote IP: ")
            r_port = int(input("Enter R-Port: "))
            tunnel_username = input("Enter remote username: ")
            Tunnel.tunnel_config[tunnel_name] = {#Adding data to tunnel_config dictionary
                "Key": ssh_key,
                "Type": tunnel_type,
                "L-Port": l_port,
                "IP": ip,
                "R-Port": r_port,
                "User": tunnel_username,
                "PID": pid
            }
            print(Tunnel.tunnel_config)
            if input("Are all the data entered correctly? Y/N: ") == "Y":
                with open("config.json", "w") as json_file:#Making a json file or opening it if existing
                    json.dump(Tunnel.tunnel_config, json_file, indent=4)#Write dictionary data into config
                    print("Writing data")
                    Tunnel.Wait(3)
            else:
                return

    def exec_tunnel():#Execute existing in config tunnels
        name_tunnel = input("Enter tunnel, which you want to execute: ")
        telnet_command = f"telnet localhost {Tunnel.tunnel_config[name_tunnel]['L-Port']}"
        tunnel_command = [
            "ssh",
             "-i", f"/home/carnifex17/.ssh/{Tunnel.tunnel_config[name_tunnel]['Key']}",
            f"-{Tunnel.tunnel_config[name_tunnel]['Type']}",
            f"{Tunnel.tunnel_config[name_tunnel]['L-Port']}:localhost:{Tunnel.tunnel_config[name_tunnel]['R-Port']}",
            "-fN", f"{Tunnel.tunnel_config[name_tunnel]['User']}@{Tunnel.tunnel_config[name_tunnel]['IP']}"
        ]
        try:
            tunnel_process = subprocess.Popen(tunnel_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"Executing {name_tunnel} tunnel (PID: {tunnel_process.pid + 1})")#Giving effect of working, but at this time process already executed or failed
            print(tunnel_command)
            tunnel_process.communicate(timeout=5)
        except subprocess.TimeoutExpired as e:
            print(f"Tunnel process timed out after {e.timeout} seconds.")
        except Exception as e:
            print(f"An error occurred: {e}")
        #finally:
            #print("SUPERKEK")
            #tunnel_process.terminate()
        try:
            telnet_process = subprocess.Popen(telnet_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = telnet_process.communicate(timeout=5) # Delete output, error =, that's for logging errors
            time.sleep(5)
            if telnet_process.returncode == 0:
                print(f"Successfully connected to the forwarded port {Tunnel.tunnel_config[name_tunnel]['L-Port']}.")
                Tunnel.tunnel_config[name_tunnel]["PID"] = tunnel_process.pid + 1 
                with open("config.json", "w") as json_file:#Making a json file or opening it if existing
                    json.dump(Tunnel.tunnel_config, json_file, indent=4)
            else:
                print(telnet_command)#This three commands are for logging commands
                print(f"Telnet Output:\n{output.decode()}")
                print(f"Telnet Error:\n{error.decode()}")
                print(f"Error: Unable to connect to the forwarded port. Telnet exit status: {telnet_process.returncode}")
        except subprocess.TimeoutExpired as e:
            print(f"Telnet process timed out after {e.timeout} seconds.")
        #except Exception as e:
         #   print(f"An error occurred: {e}")
        finally:# Terminate the tunnel process
            telnet_process.terminate()
            #tunnel_process.terminate() 
            #print(f"SUPERKEK2")
            main()

    def kill_tunnel():
        name_tunnel = input("Which Tunnel do you want to kill? ")
        if name_tunnel not in Tunnel.tunnel_config:
            print(f"Error: Tunnel '{name_tunnel}' not found.")
            return
        pid = Tunnel.tunnel_config[name_tunnel]["PID"]
        try:
            subprocess.run(['sudo', 'kill', str(pid)], check=True)
            print(f"Tunnel with PID {pid} has been killed.")
        except subprocess.CalledProcessError as e:
            print(f"Error: Unable to kill tunnel with PID {pid}. {e}")

    def Show():#Method to show json file
        with open("config.json", "r") as json_file:#Getting dictionary from config if existed
            Tunnel.tunnel_config = json.load(json_file)
        print("Looking for file")
        Tunnel.Wait(3)
        print(Tunnel.tunnel_config)
        #print(Tunnel.tunnel_config["Tunnel2"]["IP"]) ----- Parse certain data from dic
        
    def Wait(n):#Method to make waiting effect
        i = 0
        while i < n:
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
Kill
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
        if(arg=="Wait" or arg=="wait"):
            Tunnel.Wait(3)
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
        elif(arg=="Kill" or arg=="kill"):
            Tunnel.kill_tunnel()
        else:
            print("To watch all possible commands just type \'Commands\'")

if __name__ == "__main__":
    main()