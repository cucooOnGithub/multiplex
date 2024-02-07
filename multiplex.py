#-------------------------------------------------------------------------------------
# multiplex - Utility to apply a shell command to a list
#-------------------------------------------------------------------------------------
# Author    : cucoo 
# Twitter   : @cucooOnX    
# Github    : cucooOnGitHub#
#-------------------------------------------------------------------------------------
# Description : multiplex is a simple utility in python that pipe a input to a shell command.
#               You can for instance, have a list of IP addresses and execute a shell command 
#               on each one of them and pipe the results into other files
#
# Example :
#           cat list_of_ips.txt | multiplex "whois"
#-------------------------------------------------------------------------------------
import subprocess
import sys
from subprocess import Popen, PIPE

def has_positional_arguments(command):
    return any("{" + str(i) + "}" in command for i in range(10))  # Check for placeholders {0} to {9}


def process_input(input_lines, command):
    processed_lines = []

    for line in input_lines:
        if command:
            # Use subprocess to execute the specified command
            line = line.strip()
            if line == '':
                continue

            arguments = line.split(' ')
            command2=''

            if has_positional_arguments(command):
                command2 = command.format(*arguments).split(' ')            
            else:
                command2 = (command + ' ' + line).split(' ')
  
            #print(command2)
            p = Popen(command2, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            output, err = p.communicate(b"input data that is passed to subprocess' stdin")
            rc = p.returncode


            # Append both stdout and stderr to the processed lines
            processed_lines.append(output)
            processed_lines.append(err)
        else:
            # If no command is provided, pass the input line to the output without transformation
            processed_lines.append(line)

    return processed_lines

if __name__ == "__main__":
    # Check if the command-line argument is provided
    if len(sys.argv) > 1:
        # Get the command-line argument specifying the shell command
        command = sys.argv[1]
    else:
        command = None

    # Read input lines from standard input
    input_lines = sys.stdin.readlines()

    # Process the input lines using the specified command or pass through if no command is provided
    processed_lines = process_input(input_lines, command)

    # Write the result to standard output
    s = ''
    for line in processed_lines:
        if line != '':
            s+= line.decode()

    # sys.stdout.writelines(s)
    print(s, flush=True)