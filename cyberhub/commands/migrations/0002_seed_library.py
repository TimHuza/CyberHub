"""Seed the starter command library.

The data lives inside this file on purpose: a migration must keep working even
if app code changes later, so it never imports from the app. More commands are
added later with new data migrations (0003, 0004, ...).
"""

from django.db import migrations


def code(lang, *lines):
    """A fenced Markdown code block."""
    return f"```{lang}\n" + "\n".join(lines) + "\n```"


def params(*pairs):
    """A Markdown list of (flag, meaning) pairs."""
    return "\n".join(f"- `{flag}` — {meaning}" for flag, meaning in pairs)


def cmd(name, description, syntax="", parameters="", examples=""):
    return {"name": name, "description": description, "syntax": syntax, "parameters": parameters, "examples": examples}


LIBRARY = [
    {
        "name": "Python",
        "description": "Running Python, managing packages and virtual environments, and the core built-ins you use every day.",
        "categories": [
            {
                "name": "Terminal",
                "description": "Commands you type in the terminal to run Python and manage packages.",
                "commands": [
                    cmd("python --version", "Show which Python version is installed.", "python --version", examples=code("bash", "python --version")),
                    cmd("python script.py", "Run a Python file.", "python <file.py> [args]", examples=code("bash", "python hello.py", "python scanner.py 192.168.1.1")),
                    cmd("python -m venv", "Create a virtual environment: an isolated folder for one project's packages.", "python -m venv <folder>", examples=code("bash", "python -m venv venv")),
                    cmd("activate venv", "Switch the terminal to use the project's virtual environment.", "venv\\Scripts\\activate  (Windows)\nsource venv/bin/activate  (Linux/macOS)", examples=code("bash", "venv\\Scripts\\activate", "deactivate")),
                    cmd("pip install", "Install a package from PyPI into the active environment.", "pip install <package>[==version]", params(("-r <file>", "install everything listed in a requirements file"), ("--upgrade", "upgrade to the newest version")), code("bash", "pip install requests", "pip install -r requirements.txt")),
                    cmd("pip freeze", "List installed packages with exact versions, usually saved to requirements.txt.", "pip freeze", examples=code("bash", "pip freeze > requirements.txt")),
                ],
            },
            {
                "name": "Built-in Functions",
                "description": "Functions available in every Python file without importing anything.",
                "commands": [
                    cmd("print()", "Write values to the screen.", "print(*values, sep=' ', end='\\n')", params(("sep", "text placed between values"), ("end", "text added at the end (default: new line)")), code("python", 'print("Hello", "world")', 'print("a", "b", sep="-")')),
                    cmd("input()", "Ask the user for text. Always returns a string.", "input(prompt)", examples=code("python", 'name = input("Name: ")', 'age = int(input("Age: "))')),
                    cmd("len()", "Number of items in a string, list, dict or other collection.", "len(obj)", examples=code("python", 'len("hello")      # 5', "len([1, 2, 3])   # 3")),
                    cmd("type()", "Show the type of a value.", "type(obj)", examples=code("python", "type(42)       # <class 'int'>", 'type("42")     # <class \'str\'>')),
                    cmd("range()", "A sequence of numbers, mostly used in for loops.", "range(stop) / range(start, stop, step)", examples=code("python", "for i in range(5):", "    print(i)   # 0..4", "list(range(1, 10, 2))   # [1, 3, 5, 7, 9]")),
                ],
            },
            {
                "name": "Files",
                "description": "Reading and writing files.",
                "commands": [
                    cmd("open()", "Open a file and return a file object.", "open(path, mode='r', encoding='utf-8')", params(("r", "read (default)"), ("w", "write — replaces the file"), ("a", "append to the end"), ("b", "binary, e.g. rb")), code("python", 'f = open("notes.txt", encoding="utf-8")', "text = f.read()", "f.close()")),
                    cmd("with open()", "Open a file and close it automatically, even if an error happens. The recommended way.", "with open(path, mode) as f:", examples=code("python", 'with open("notes.txt", encoding="utf-8") as f:', "    for line in f:", "        print(line.strip())")),
                    cmd("f.read()", "Read the whole file as one string.", "f.read()", examples=code("python", 'with open("log.txt") as f:', "    content = f.read()")),
                    cmd("f.write()", "Write a string to a file opened with w or a.", "f.write(text)", examples=code("python", 'with open("out.txt", "w", encoding="utf-8") as f:', '    f.write("Scan finished\\n")')),
                ],
            },
        ],
    },
    {
        "name": "Networking",
        "description": "Testing connectivity, routes, DNS and interfaces on Windows and Linux.",
        "categories": [
            {
                "name": "Reachability",
                "description": "Check whether a host can be reached and which path packets take.",
                "commands": [
                    cmd("ping", "Send ICMP echo requests to check if a host replies and how fast.", "ping [options] <host>", params(("-c <n>", "Linux: stop after n packets"), ("-n <n>", "Windows: number of packets"), ("-t", "Windows: ping until stopped (Ctrl+C)")), code("bash", "ping -c 4 8.8.8.8", "ping -n 4 google.com")),
                    cmd("traceroute", "Linux: show every router (hop) on the path to a host.", "traceroute [options] <host>", params(("-n", "show IP addresses only, no DNS names (faster)"),), code("bash", "traceroute -n 8.8.8.8")),
                    cmd("tracert", "Windows: show every router (hop) on the path to a host.", "tracert [options] <host>", params(("-d", "don't resolve names (faster)"),), code("bat", "tracert -d 8.8.8.8")),
                ],
            },
            {
                "name": "Route",
                "description": "View the routing table: where the system sends traffic for each network.",
                "commands": [
                    cmd("route print", "Windows: show the routing table.", "route print", examples=code("bat", "route print -4")),
                    cmd("ip route", "Linux: show or change the routing table.", "ip route [show | add | del] ...", examples=code("bash", "ip route", "ip route get 8.8.8.8")),
                    cmd("netstat -r", "Show the routing table (works on Windows and Linux).", "netstat -r", examples=code("bash", "netstat -rn")),
                ],
            },
            {
                "name": "DNS",
                "description": "Resolve names to IP addresses and troubleshoot DNS.",
                "commands": [
                    cmd("nslookup", "Ask a DNS server for the records of a name.", "nslookup [-type=<record>] <name> [server]", params(("-type=A|AAAA|MX|NS|TXT", "which record type to ask for"),), code("bash", "nslookup example.com", "nslookup -type=MX example.com 1.1.1.1")),
                    cmd("dig", "Linux: detailed DNS query tool.", "dig [@server] <name> [type]", params(("+short", "show only the answer"),), code("bash", "dig example.com", "dig @1.1.1.1 example.com MX +short")),
                    cmd("ipconfig /flushdns", "Windows: clear the local DNS cache.", "ipconfig /flushdns", examples=code("bat", "ipconfig /flushdns")),
                ],
            },
            {
                "name": "Interfaces & Ports",
                "description": "See your IP configuration and which ports are open or connected.",
                "commands": [
                    cmd("ipconfig", "Windows: show IP address, mask and gateway of each adapter.", "ipconfig [/all]", params(("/all", "also show MAC address, DNS servers and DHCP info"),), code("bat", "ipconfig /all")),
                    cmd("ip addr", "Linux: show interfaces and their IP addresses.", "ip addr [show <interface>]", examples=code("bash", "ip addr", "ip a show eth0")),
                    cmd("netstat -ano", "Windows: list connections and listening ports with the owning process ID.", "netstat -ano", params(("-a", "all connections and listening ports"), ("-n", "numbers instead of names"), ("-o", "show process ID (PID)")), code("bat", 'netstat -ano | findstr ":443"')),
                    cmd("ss -tulpn", "Linux: list listening TCP/UDP ports and the programs using them.", "ss [options]", params(("-t / -u", "TCP / UDP"), ("-l", "listening sockets only"), ("-p", "show process"), ("-n", "numbers instead of names")), code("bash", "sudo ss -tulpn")),
                ],
            },
        ],
    },
    {
        "name": "Linux",
        "description": "Everyday Linux terminal commands: moving around, files, permissions, processes and packages.",
        "categories": [
            {
                "name": "Navigation",
                "description": "Find out where you are and move around the file system.",
                "commands": [
                    cmd("pwd", "Print the current directory.", "pwd", examples=code("bash", "pwd")),
                    cmd("ls", "List files in a directory.", "ls [options] [path]", params(("-l", "long format: permissions, owner, size, date"), ("-a", "include hidden files"), ("-h", "human-readable sizes")), code("bash", "ls -lah /etc")),
                    cmd("cd", "Change directory.", "cd <path>", params(("..", "go up one level"), ("~", "go to your home directory"), ("-", "go back to the previous directory")), code("bash", "cd /var/log", "cd ..")),
                    cmd("find", "Search for files by name, type, size and more.", "find <path> [tests]", params(("-name", "match a file name pattern"), ("-type f|d", "files or directories only")), code("bash", 'find / -name "*.conf" 2>/dev/null')),
                ],
            },
            {
                "name": "Files & Permissions",
                "description": "Copy, move and delete files, and control who can read, write or run them.",
                "commands": [
                    cmd("cp", "Copy files or directories.", "cp [options] <source> <destination>", params(("-r", "copy directories recursively"),), code("bash", "cp notes.txt backup/", "cp -r project/ project_copy/")),
                    cmd("mv", "Move or rename files.", "mv <source> <destination>", examples=code("bash", "mv old.txt new.txt")),
                    cmd("rm", "Delete files. There is no recycle bin — deleted means gone.", "rm [options] <file>", params(("-r", "delete directories and their contents"), ("-i", "ask before each delete")), code("bash", "rm -i test.txt")),
                    cmd("chmod", "Change permissions (read, write, execute).", "chmod <mode> <file>", params(("u/g/o", "user (owner), group, others"), ("r=4 w=2 x=1", "numeric values, e.g. 755")), code("bash", "chmod +x script.sh", "chmod 600 id_rsa")),
                    cmd("chown", "Change the owner and group of a file.", "chown <user>[:group] <file>", examples=code("bash", "sudo chown tim:tim report.txt")),
                ],
            },
            {
                "name": "Processes",
                "description": "See what is running and stop programs.",
                "commands": [
                    cmd("ps", "Show running processes.", "ps [options]", params(("aux", "all processes from all users, with details"),), code("bash", "ps aux | grep ssh")),
                    cmd("top", "Live view of processes sorted by CPU usage. Press q to quit.", "top", examples=code("bash", "top")),
                    cmd("kill", "Send a signal to a process, normally to stop it.", "kill [-signal] <PID>", params(("-15", "ask politely to stop (default)"), ("-9", "force stop immediately")), code("bash", "kill 1234", "kill -9 1234")),
                ],
            },
            {
                "name": "Packages",
                "description": "Install and update software on Debian/Ubuntu/Kali with apt.",
                "commands": [
                    cmd("apt update", "Refresh the list of available packages. Run before installing.", "sudo apt update", examples=code("bash", "sudo apt update")),
                    cmd("apt upgrade", "Upgrade all installed packages to their newest versions.", "sudo apt upgrade", examples=code("bash", "sudo apt update && sudo apt upgrade -y")),
                    cmd("apt install", "Install a package.", "sudo apt install <package>", params(("-y", "answer yes to prompts automatically"),), code("bash", "sudo apt install nmap")),
                    cmd("apt remove", "Uninstall a package.", "sudo apt remove <package>", examples=code("bash", "sudo apt remove nmap")),
                ],
            },
        ],
    },
    {
        "name": "PowerShell",
        "description": "Windows PowerShell cmdlets for help, files, processes, services and networking.",
        "categories": [
            {
                "name": "Help & Discovery",
                "description": "Find commands and learn how to use them — PowerShell documents itself.",
                "commands": [
                    cmd("Get-Help", "Show help for a cmdlet.", "Get-Help <cmdlet> [-Examples | -Full]", params(("-Examples", "show only usage examples"), ("-Full", "show everything")), code("powershell", "Get-Help Get-Process -Examples")),
                    cmd("Get-Command", "Find cmdlets by name or verb.", "Get-Command [-Verb <verb>] [-Noun <noun>] [name]", examples=code("powershell", "Get-Command *service*", "Get-Command -Verb Get -Noun Net*")),
                    cmd("Get-Member", "Show the properties and methods of objects in the pipeline.", "<command> | Get-Member", examples=code("powershell", "Get-Process | Get-Member")),
                ],
            },
            {
                "name": "Files",
                "description": "Work with files and folders.",
                "commands": [
                    cmd("Get-ChildItem", "List files and folders (alias: ls, dir).", "Get-ChildItem [path] [-Recurse] [-Filter <pattern>]", params(("-Recurse", "include subfolders"), ("-Force", "include hidden files")), code("powershell", "Get-ChildItem C:\\Users -Recurse -Filter *.txt")),
                    cmd("Set-Location", "Change directory (alias: cd).", "Set-Location <path>", examples=code("powershell", "Set-Location C:\\Projects")),
                    cmd("Get-Content", "Read a file's contents (alias: cat).", "Get-Content <path> [-Tail <n>]", params(("-Tail <n>", "only the last n lines"), ("-Wait", "keep reading new lines, like tail -f")), code("powershell", "Get-Content .\\log.txt -Tail 20")),
                    cmd("Copy-Item", "Copy files or folders (alias: cp).", "Copy-Item <source> <destination> [-Recurse]", examples=code("powershell", "Copy-Item .\\report.txt D:\\Backup\\")),
                    cmd("Remove-Item", "Delete files or folders (alias: rm).", "Remove-Item <path> [-Recurse]", params(("-WhatIf", "show what would be deleted without deleting"),), code("powershell", "Remove-Item .\\temp -Recurse -WhatIf")),
                ],
            },
            {
                "name": "Processes & Services",
                "description": "Inspect and control running programs and Windows services.",
                "commands": [
                    cmd("Get-Process", "List running processes.", "Get-Process [name]", examples=code("powershell", "Get-Process | Sort-Object CPU -Descending | Select-Object -First 5")),
                    cmd("Stop-Process", "Stop a process by name or ID.", "Stop-Process -Name <name> | -Id <PID>", examples=code("powershell", "Stop-Process -Name notepad")),
                    cmd("Get-Service", "List Windows services and their status.", "Get-Service [name]", examples=code("powershell", "Get-Service | Where-Object Status -eq Running")),
                    cmd("Restart-Service", "Restart a service (needs an administrator PowerShell).", "Restart-Service <name>", examples=code("powershell", "Restart-Service Spooler")),
                ],
            },
            {
                "name": "Networking",
                "description": "PowerShell versions of ping, ipconfig and nslookup.",
                "commands": [
                    cmd("Test-NetConnection", "Ping a host or test whether a TCP port is open.", "Test-NetConnection <host> [-Port <n>]", params(("-Port <n>", "test a TCP port"), ("-TraceRoute", "also show the route")), code("powershell", "Test-NetConnection google.com -Port 443")),
                    cmd("Get-NetIPAddress", "Show IP addresses of the network adapters.", "Get-NetIPAddress [-AddressFamily IPv4]", examples=code("powershell", "Get-NetIPAddress -AddressFamily IPv4")),
                    cmd("Resolve-DnsName", "Look up DNS records.", "Resolve-DnsName <name> [-Type <record>]", examples=code("powershell", "Resolve-DnsName example.com -Type MX")),
                ],
            },
        ],
    },
    {
        "name": "Bash",
        "description": "Bash shell scripting on Linux — the Unix counterpart to PowerShell: variables, conditions, loops, pipes and redirection.",
        "categories": [
            {
                "name": "Variables & Output",
                "description": "Store values and print them.",
                "commands": [
                    cmd("echo", "Print text or variables.", "echo [options] <text>", params(("-n", "no new line at the end"), ("-e", "understand \\n and \\t")), code("bash", 'echo "Hello $USER"')),
                    cmd("VAR=value", "Create a variable. No spaces around =. Read it with $VAR.", "NAME=value", examples=code("bash", "TARGET=10.0.0.5", 'echo "Scanning $TARGET"')),
                    cmd("read", "Read a line of input from the user into a variable.", "read [-p prompt] <var>", params(("-p", "show a prompt"), ("-s", "silent, for passwords")), code("bash", 'read -p "Host: " HOST')),
                    cmd("$(command)", "Command substitution: use a command's output as a value.", "$(command)", examples=code("bash", "TODAY=$(date +%F)", 'echo "Report for $TODAY"')),
                ],
            },
            {
                "name": "Conditions & Loops",
                "description": "Make decisions and repeat work in scripts.",
                "commands": [
                    cmd("if", "Run commands only when a condition is true.", "if [ condition ]; then ... elif ...; else ...; fi", params(("-f file", "file exists"), ("-d dir", "directory exists"), ("-eq -ne -lt -gt", "number comparisons"), ("= !=", "text comparisons")), code("bash", "if [ -f /etc/passwd ]; then", '    echo "found"', "fi")),
                    cmd("for", "Repeat commands for each item in a list.", "for VAR in list; do ...; done", examples=code("bash", "for ip in 10.0.0.{1..5}; do", "    ping -c 1 $ip", "done")),
                    cmd("while", "Repeat commands while a condition is true.", "while [ condition ]; do ...; done", examples=code("bash", "while read -r line; do", '    echo "$line"', "done < hosts.txt")),
                ],
            },
            {
                "name": "Pipes & Redirection",
                "description": "Connect commands together and send output to files.",
                "commands": [
                    cmd("|", "Pipe: send one command's output into the next command.", "command1 | command2", examples=code("bash", "cat auth.log | grep Failed | wc -l")),
                    cmd(">", "Write output to a file, replacing what was there.", "command > file", examples=code("bash", "ls -la > listing.txt")),
                    cmd(">>", "Append output to the end of a file.", "command >> file", examples=code("bash", 'echo "done" >> scan.log')),
                    cmd("2>", "Redirect error messages (stderr). 2>/dev/null hides them.", "command 2> file", examples=code("bash", 'find / -name "*.key" 2>/dev/null')),
                    cmd("grep", "Show only lines that match a pattern.", "grep [options] <pattern> [file]", params(("-i", "ignore case"), ("-r", "search folders recursively"), ("-n", "show line numbers"), ("-v", "show lines that do NOT match")), code("bash", 'grep -in "error" /var/log/syslog')),
                ],
            },
        ],
    },
    {
        "name": "Git",
        "description": "Version control with Git and GitHub: set up, save snapshots, branch and sync.",
        "categories": [
            {
                "name": "Setup & Configuration",
                "description": "These commands set your identity and create or copy repositories.",
                "commands": [
                    cmd("git config", "Set your name, email and other settings.", "git config [--global] <key> <value>", params(("--global", "apply to all your repositories"), ("--list", "show current settings")), code("bash", 'git config --global user.name "Your Name"', 'git config --global user.email "you@example.com"')),
                    cmd("git init", "Turn the current folder into a new Git repository.", "git init", examples=code("bash", "git init")),
                    cmd("git clone", "Download a copy of a remote repository.", "git clone <url> [folder]", examples=code("bash", "git clone https://github.com/user/repo.git")),
                ],
            },
            {
                "name": "Staging & Snapshots",
                "description": "Choose changes and save them as commits.",
                "commands": [
                    cmd("git status", "Show changed, staged and untracked files.", "git status [-s]", params(("-s", "short format"),), code("bash", "git status")),
                    cmd("git add", "Stage changes so they go into the next commit.", "git add <file | .>", params((".", "stage everything in the current folder"), ("-p", "choose parts of files interactively")), code("bash", "git add models.py", "git add .")),
                    cmd("git commit", "Save the staged changes as a snapshot with a message.", 'git commit -m "<message>"', examples=code("bash", 'git commit -m "feat: add login page"')),
                    cmd("git diff", "Show what changed in files.", "git diff [--staged] [file]", params(("--staged", "changes already staged for commit"),), code("bash", "git diff", "git diff --staged")),
                    cmd("git log", "Show commit history.", "git log [options]", params(("--oneline", "one short line per commit"), ("--graph", "draw branches")), code("bash", "git log --oneline --graph")),
                ],
            },
            {
                "name": "Branching",
                "description": "Work on features separately, then combine them.",
                "commands": [
                    cmd("git branch", "List, create or delete branches.", "git branch [name] [-d name]", params(("-d", "delete a merged branch"), ("-a", "include remote branches")), code("bash", "git branch", "git branch -d old-feature")),
                    cmd("git switch", "Move to another branch.", "git switch [-c] <branch>", params(("-c", "create the branch and switch to it"),), code("bash", "git switch -c feat/clv", "git switch main")),
                    cmd("git merge", "Bring another branch's commits into the current branch.", "git merge <branch>", examples=code("bash", "git switch main", "git merge feat/clv")),
                ],
            },
            {
                "name": "Remote (GitHub)",
                "description": "Connect to GitHub and keep both copies in sync.",
                "commands": [
                    cmd("git remote add", "Link the local repository to a remote one, usually called origin.", "git remote add <name> <url>", examples=code("bash", "git remote add origin https://github.com/user/repo.git", "git remote -v")),
                    cmd("git push", "Upload local commits to the remote.", "git push [-u] <remote> <branch>", params(("-u", "remember the remote branch, so later plain git push works"),), code("bash", "git push -u origin main")),
                    cmd("git pull", "Download remote commits and merge them into the current branch.", "git pull [remote] [branch]", examples=code("bash", "git pull origin main")),
                    cmd("git fetch", "Download remote commits without changing your files.", "git fetch [remote]", examples=code("bash", "git fetch origin")),
                ],
            },
        ],
    },
]


def seed_library(apps, schema_editor):
    # apps.get_model gives the model as it was at this migration, not today's code.
    Tab = apps.get_model("commands", "Tab")
    Category = apps.get_model("commands", "Category")
    Command = apps.get_model("commands", "Command")

    for tab_order, tab_data in enumerate(LIBRARY, start=1):
        tab = Tab.objects.create(name=tab_data["name"], description=tab_data["description"], order=tab_order)
        for category_order, category_data in enumerate(tab_data["categories"], start=1):
            category = Category.objects.create(tab=tab, name=category_data["name"], description=category_data["description"], order=category_order)
            for command_order, command_data in enumerate(category_data["commands"], start=1):
                Command.objects.create(category=category, order=command_order, **command_data)


def remove_library(apps, schema_editor):
    """Undo: delete children first, because RESTRICT blocks deleting a parent that has children."""
    apps.get_model("commands", "Command").objects.all().delete()
    apps.get_model("commands", "Category").objects.all().delete()
    apps.get_model("commands", "Tab").objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("commands", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_library, remove_library),
    ]
