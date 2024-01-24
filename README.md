# multiplex

multiplex is a simple utility in python that pipes a input to a shell command.

# How does it work?

multiplex reads all the lines it receives from from the standard inout and applies then the bash shell command, that you specified as parameter.

# Usage

Provide some list via stdin, and pass the command that you wish to apply for each of that list as a input parameter to the command.

Example: 

```
    cat list_of_ips.txt | multiplex "whois"
```

# Output

Outputs the result of applying the command to each line

# Output example

```
# cat domains.txt                        
google.com
apple.com
microsoft.com

# cat domains.txt | python3 multiplex.py "digg +short"
142.250.184.14
17.253.144.10
20.112.250.133
20.236.44.162
20.70.246.20
20.76.201.171
20.231.239.246

```

# Installation

Just copy the python scritp to a location in your environment path.
