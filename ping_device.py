import subprocess
import threading

NUM_THREADS = 10  # Number of threads for concurrent pinging

# Function for pinging and saving results
def ping_and_save(ip):
    cmd = f"ping -n 4 {ip}"  # Ping command for the given IP address
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    response = result.stdout
    
    # Check if the host responded at least 3 times and determine status
    with open("ip_output.txt", "a") as f:
        if response.count("Reply from") >= 3:
            status = "OK"
        else:
            status = "DOWN!!!"
            
        print(response)  # Display ping response on the console
        f.write(f"{ip} = {status}\n")  # Save results to the output file

# Clearing the ip_output.txt file
open("ip_output.txt", "w").close()

# Ping for each IP in the file
with open("ip_list.txt") as file:
    ip_list = file.read()
    ip_list = ip_list.splitlines()
    print(f"{ip_list}\n")

threads = []
for ip in ip_list:
    thread = threading.Thread(target=ping_and_save, args=(ip,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

# Display the content of the output file on the screen
print('------------------------------------------------------\n')
with open("ip_output.txt") as file:
    output = file.read()
    print(output)
print('------------------------------------------------------\n')

input('Press ENTER to exit...')
