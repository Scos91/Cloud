# Cloud Security Project: Attack & Defense Suite

This project simulates DoS/DDoS attack scenarios and real-time detection & mitigation in a virtualized Linux environment using GUI-based tools.

This project contains two GUIs, four attack .py scripts and four corresponding defense scripts. The atkGUI (with built in attack scripts ([VM-Network], [VM-Host], [Container-Network], and [Container-Host])) and a defGUI (with built in defense scripts - to detect/ mitigate the attacks) serve as automated tools to run the tests and log the metrics surrounding the attack and coresponding defensive detection/ mitigation. After running any attack the metrics are aggregated and outputted to attackLog.txt. Similarly, when running any one of the defenses, each will output their concerned metrics to a .log file (cpuBurnDef.py -> cpuBurnDef.log; frkBombDef.py -> frkBombDef.log; httpFloodDef.py -> httpFloodDef.log; synDef1.py -> synDefense.log) that can be reviewed to further investigate what is taking place during detection/ mitigation of an attack. 

The network attacks assume that two different machines (hardware or VM - as long as they can ping each other it shouldn't matter) are being used - the premise being that an 'attacker' is attacking a target machine. The host attacks are assumed to be ran on a singular machine (hardare or VM) - the premise being that the 'attacker' had gained persistence on the machine, planted a malicious script (i.e. the attack script), and then launched it either through direct SSH access, or a C&C server. 

The [VM-Network] attack is modeled after a SYN flood style attack wherein multiple SYN handshakes occur, causing a DOS of the target machine. When running the [VM-Network] attack start by using - 'sudo python3 -m http.server 80' (on the defending VM) before initiating the monitor and then switching to, queuing up, and launching the attack from the attack VM. 

The [VM-Host] attack is modeled after a CPU exhaustion or 'runaway process' style attack, where one or multiple processes are designed to take up a large portion, if not all, of CPU, memory, or both on the target machine leading to DOS. When running the [VM-Host] attack start the monitor from the defGUI and then swap to the atkGUI to queue up and launch the corresponding attack. 

The [Container-Network] attack is modeled after an HTTP flood style attack wherein multiple HTTP requests are sent to the running web-oriented container with the intention of causing a DOS. When running the [Container-Network] attack start with creating the 'web' container - 'docker run -d -p 80:80 --name web nginx', once done start the container - 'sudo docker start web', and then check that it is running - 'sudo docker ps'. Once 'web' is running, the monitor can be started from the def VM running the defGUI and the attack can be queued and launched from the atk VM running the atkGUI.

The [Container-Host] attack is modeled after a 'fork-bomb' style attack, wherein a script is run to generate multiple parent/ children processes that keep forking and ultimately end up using all available resources on the machine, resulting in a DOS. When running the [Container-Host] attack start with creating the 'web' container - 'docker run -d -p 80:80 --name web nginx', once done start the container - 'sudo docker start web', and then check that it is running - 'sudo docker ps'. Once 'web' is running, the monitor can be started from the defGUI and the attack can be queued and launched from the atkGUI. **NOTE - It is important to note that the mitigation for this attack involves stopping the container first and then restarting it ten seconds later - if the monitor is stopped from the defGUI, prematurely, then the restart will not occur.**

**NOTE - for network attacks, detection, and mitigation; you cannot have 'sudo python3 -m http.server 80' and the 'web' container ('docker run -d -p 80:80 --name web nginx') running at the same time, they will fight for the port. Either stop the container before starting the http.server, or vice-versa.**

**NOTE - The VMs used when testing the funcitonality of this project code had the network adapter set to: `Bridged Adapter`.**

---

## Quick Start

> This project includes two GUIs:
> - `atkGUI.py` — Launch and control simulated network/host-based attacks.
-----> Outputs 'attackLog.txt' when ran — aggregation of metrics associated with each attack committed.
> - `defGUI.py` — Monitor, detect, and mitigate those attacks in real time.

> Four separate attack scripts (utilized by atkGUI.py):
> - `synAtkVm.py` — integrated into the 'VM Network' tab of the atkGUI — simulates SYN flood on target.
> - `burnCPU_VmHost.py` — integrated into the 'VM Host' tab of the atkGUI — simulates a runaway process attack.
> - `httpFlood_Container.py` — integrated into the 'Container Network' tab of the atkGUI — simulates a HTTP flood on the target.
> - `frkBombHost_Container.py` — integrated into the 'Container Host' tab of the atkGUI — simulates a Fork Bomb attack on the target.

> Four separate defense scripts — for detection and mitigation of host system (utilized by defGUI.py):
> - `synDef1.py` — integrated into the 'SYN Monitor' button on the defGUI — protects from SYN Flood, provides user input thresholds, blocks offending IPs and allows for the unblocking of those same IPs.
-----> Outputs 'synDefense.log' and 'syn_blocked_ips.txt' when ran.
> - `cpuBurnDef.py` — integrated into the 'CPU Monitor' button on the defGUI — protects from runaway processes, alerts are piped into the log located on the spawned window.
-----> Outputs 'cpuBurnDef.log' when ran.
> - `httpFloodDef.py` — integrated into the 'HTTP Monitor' button on the defGUI — protects from HTTP Flood, provides user input thresholds, blocks offending IPs and allows for the unblocking of those same IPs.
-----> Outputs 'httpFloodDef.log' and 'http_blocked_ips.txt' when ran.
> - `frkBombDef.py` — integrated into the 'Fork Bomb Monitor' button on the defGUI — protects from Fork Bomb, alerts are piped into the log located on the spawned window. **NOTE - if monitor is stopped prematurely, full mitigation will not occur, see above.**
-----> Outputs 'frkBombDef.log' when ran.

---

## Setup Options

### Recommended (One-Step Install) (Run on Both VMs)

1. Open a terminal in the project folder.
2. Run: ./setup.sh

### If One-Step Install Not Working

1. sudo apt update && sudo apt upgrade -y
2. sudo apt install -y python3 python3-pip python3-venv git curl wget nano
3. sudo apt install -y docker.io
4. sudo systemctl start docker
5. sudo systemctl enable docker
6. sudo usermod -aG docker $USER
7. [reboot - to take effect]
8. cd <folder containing project code>
9. python3 -m venv venv
10. source venv/bin/activate
11. pip install --upgrade pip
12. pip install pyqt5 psutil psycopg2-binary bcrypt matplotlib
13. [optional] chmod +x defGUI.py atkGUI.py
14. deactivate
15. [reboot]

— GUI Launch —
1. cd <folder containing project code>
2. source venv/bin/activate
3. sudo python3 <atk/def>GUI.py

---

### Required Packages/ Denpendencies

> - python3
> - python3-pip
> - python3-venv
> - docker.io
> - git
> - curl
> - wget
> - pyqt5
> - psutil
> - bcrypt
> - matplotlib
> - iptables
> - hping3 (should be installed, if not - sudo apt install -y hping3)
> - apache2-utils (should be installed, if not - sudo apt install -y apache2-utils)

---

### Running program - Testing Attacks
_________________________________________________________________________________________________________________________________________________________________________________________________________________________
#### [VM-Network] Attack/ Detection/ Mitigation ####

**2 VMs or Machines**

**DEF**
[system1 - terminal window - 1]
> - Open a terminal in the project folder.
> - cd <folder containing project code> 
> - source venv/bin/activate
> - sudo python3 defGUI.py

[system1 - terminal window - 2]
> - ip a                                                                    **note the ip address this will be designated as def_VM_IP going forward**
> - ping <atk_VM_IP>                                                        **ensure you can ping atk_VM_IP before proceeding**
> - sudo python3 -m http.server 80                                          **need something on port 80 for test, I used basic http.server**

[system1 - terminal window - 1]
> - **click `SYN Monitor` button**
> - **click `Start SYN Defense` button**
> - **should now see that the atk_VM_IP is blocked - under `Blocked IPs:`**
> - **click `Stop SYN Defense` button**

— ONCE ATTACK CONCLUDED —
[system1 - terminal window - 3]
> - sudo iptables -L -n | grep DROP                                         **ensure that atk_VM_IP is now blocked**

[system1 - terminal window - 1]
> - **highlight blocked IP**
> - **click `Unblock Selected IP` button**

[system1 - terminal window - 3]
> - sudo iptables -L -n | grep DROP                                         **ensure that atk_VM_IP is now un-blocked**

[system1 - terminal window - 2]
> - **Ctrl + C - on http.server command**                                   **http.server needs to be stopped for container testing**

**ATK**
[system2 - terminal window - 1]
> - Open a terminal in the project folder.
> - cd <folder containing project code> 
> - source venv/bin/activate
> - sudo python3 atkGUI.py 

[system2 - terminal window - 2]
> - ip a                                                                    **note the ip address this will be designated as atk_VM_IP going forward**
> - ping <def_VM_IP>                                                        **ensure you can ping def_VM_IP before proceeding**

[system2 - terminal window - 1]
> - **verify that you are in `VM Network` tab**
> - **change `Target IP` input field to <def_VM_IP>**
— ONCE SYN MONITOR IS RUNNING —
> - **click `Launch VM Network-Based Attack` to launch**

— ONCE ATTACK CONCLUDED —
[system2 - terminal window - 2]
> - ping <def_VM_IP>                                                        **ensure you can't ping def_VM_IP - you should now be blocked**
— ONCE CONFIRMED UNBLOCKED —
> - ping <def_VM_IP>                                                        **ensure you can ping def_VM_IP - you should now be un-blocked**

**NOTE - all traffic and actions taken by GUIs are accessible in their respective .log/ .txt files located in the project folder**

_________________________________________________________________________________________________________________________________________________________________________________________________________________________
#### [VM-Host] Attack/ Detection/ Mitigation ####

**All on one VM or machine**

**DEF**
[terminal window - 1]
> - Open a terminal in the project folder.
> - cd <folder containing project code> 
> - source venv/bin/activate
> - sudo python3 defGUI.py
> - **click `CPU Monitor` button**
> - **click `Start CPU Monitor` button**
— ONCE ATTACK IS RUNNING —
> - **you should see normal CPU usage until the attack is launched, then there be an alert for `High CPU usage...` - it will analyze the op processes and kill the ones causing the exhaustion attacks**
> - **click `Stop CPU Monitor` button**

**ATK**
[terminal window - 1]
> - Open a terminal in the project folder.
> - cd <folder containing project code> 
> - source venv/bin/activate
> - sudo python3 atkGUI.py 
> - **click `VM Host` tab**
— ONCE MONITOR IS RUNNING —
> - **click `Launch VM Host-Based Attack`**

**NOTE - all traffic and actions taken by GUIs are accessible in their respective .log files located in the project folder**

_________________________________________________________________________________________________________________________________________________________________________________________________________________________
#### [Container-Network] Attack/ Detection/ Mitigation ####

**2 VMs or Machines**

**DEF**
[system1 - terminal window - 1]
> - Open a terminal in the project folder.
> - cd <folder containing project code> 
> - source venv/bin/activate
> - sudo python3 defGUI.py

[system1 - terminal window - 2]
> - ip a                                                                    **note the ip address this will be designated as def_VM_IP going forward**
> - ping <atk_VM_IP>                                                        **ensure you can ping atk_VM_IP before proceeding**
> - sudo docker run -d -p 80:80 --name web nginx                            **if the container is already created, you do not need to run this again; proceed to next step**
> - sudo docker start web                                                   **if http.server is still running, this will not work**
> - sudo docker ps                                                          **confirm, you should see a container 'web'**

[system1 - terminal window - 1]
> - **click `HTTP Monitor` button**
> - **click `Start HTTP Monitor` button**
> - **should now see that the atk_VM_IP is blocked - under `Blocked IPs:`**
> - **click `Stop HTTP Monitor` button**

— ONCE ATTACK CONCLUDED —
[system1 - terminal window - 2]
> - sudo iptables -L -n | grep DROP                                         **ensure that atk_VM_IP is now blocked**

[system1 - terminal window - 1]
> - **highlight blocked IP**
> - **click `Unblock Selected IP` button**

[system1 - terminal window - 2]
> - sudo iptables -L -n | grep DROP                                         **ensure that atk_VM_IP is now un-blocked**

**ATK**
[system2 - terminal window - 1]
> - Open a terminal in the project folder.
> - cd <folder containing project code> 
> - source venv/bin/activate
> - sudo python3 atkGUI.py 

[system2 - terminal window - 2]
> - ip a                                                                    **note the ip address this will be designated as atk_VM_IP going forward**
> - ping <def_VM_IP>                                                        **ensure you can ping def_VM_IP before proceeding**

[system2 - terminal window - 1]
> - **verify that you are in `Container Network` tab**
> - **change `Target IP` input field to <def_VM_IP>**
> - **change `Port` input field to 80**
— ONCE SYN MONITOR IS RUNNING —
> - **click `Launch VM Network-Based Attack` to launch**

— ONCE ATTACK CONCLUDED —
[system2 - terminal window - 2]
> - ping <def_VM_IP>                                                        **ensure you can't ping def_VM_IP - you should now be blocked**
— ONCE CONFIRMED UNBLOCKED —
> - ping <def_VM_IP>                                                        **ensure you can ping def_VM_IP - you should now be un-blocked**

**NOTE - all traffic and actions taken by GUIs are accessible in their respective .log/ .txt files located in the project folder**

_________________________________________________________________________________________________________________________________________________________________________________________________________________________
#### [Container-Host] Attack/ Detection/ Mitigation ####

**All on one VM or machine**

**DEF**
[terminal window - 1]
> - Open a terminal in the project folder.
> - cd <folder containing project code> 
> - source venv/bin/activate
> - sudo python3 defGUI.py
> - **click `Fork Bomb Monitor` button**
> - **click `Start Fork Bomb Monitor` button**
— ONCE ATTACK IS RUNNING —
> - **you should see a process count for the container once attack is launched, then there be an alert for `Timeout: container 'web'...` being unresponsive, then the mitigation will stop the container and a countdown will start to restart the container**
> - **click `Stop CPU Monitor` button**

**ATK**
[terminal window - 1]
> - Open a terminal in the project folder.
> - cd <folder containing project code> 
> - source venv/bin/activate
> - sudo python3 atkGUI.py 
> - **click `Container Host` tab**
— ONCE MONITOR IS RUNNING —
> - **click `Launch VM Host-Based Attack`**

**NOTE - all traffic and actions taken by GUIs are accessible in their respective .log files located in the project folder**
**NOTE - with number of forks set to 50, the GUIs might stall, if so just wait for it to pick back up; if it freezes, close and reopen then reduce the forks to 20**