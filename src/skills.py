# src/skills.py
import subprocess
import os
import webbrowser
import datetime
import psutil

class KiraSkills:
    def execute(self, command_tag):
        """
        Executes specific actions OR arbitrary terminal commands.
        """
        # Clean up the tag to get the raw action
        action = command_tag.replace("[CMD:", "").replace("]", "").strip()
        
        print(f"[System] Executing Skill: {action}")
        
        try:
            # --- 1. UNIVERSAL TERMINAL CONTROL (UPDATED FOR SAFETY) ---
            if action.startswith("terminal:"):
                cmd = action.replace("terminal:", "").strip()
                
                # We construct a compound bash command:
                # 1. Clear screen
                # 2. Print the command in Green color ([KIRA EXEC])
                # 3. Print a separator line
                # 4. Run the actual command
                # 5. Keep shell open (exec bash)
                
                safe_command = (
                    f"clear; "
                    f"echo -e '\\e[1;32m[KIRA] I am executing this command:\\e[0m'; "
                    f"echo -e '\\e[1;37m{cmd}\\e[0m'; "
                    f"echo '----------------------------------------'; "
                    f"{cmd}; "
                    f"exec bash"
                )

                # Launch Konsole with this safe wrapper
                subprocess.Popen(["konsole", "-e", "bash", "-c", safe_command])
                return f"Executed terminal command: {cmd}"

            # --- 2. UNIVERSAL SYSTEM SEARCH ---
            elif action.startswith("search_system:"):
                query = action.replace("search_system:", "").strip()
                try:
                    # Using 'plocate' or 'locate'
                    result = subprocess.check_output(f"locate -i -l 5 '{query}'", shell=True).decode("utf-8")
                    if not result:
                        return f"I couldn't find anything matching '{query}'."
                    return f"Found these files:\n{result}"
                except:
                    return "Search failed. (Make sure 'plocate' is installed)."

            # --- 3. POWER CONTROL ---
            elif action == "shutdown_system":
                # Safety check for shutdown
                subprocess.Popen(["konsole", "-e", "bash", "-c", "echo 'Shutdown requested. Type sudo password to confirm.'; sudo shutdown now; exec bash"])
                return "Shutting down..."
            elif action == "reboot_system":
                subprocess.Popen(["konsole", "-e", "bash", "-c", "echo 'Reboot requested. Type sudo password to confirm.'; sudo reboot; exec bash"])
                return "Rebooting..."

            # --- EXISTING BASIC SKILLS ---
            elif action == "open_terminal":
                subprocess.Popen(["konsole"])
                return "Terminal launched."
            elif action == "open_browser":
                # Tries to open default browser
                webbrowser.open("https://google.com")
                return "Browser opened."
            elif action == "open_files":
                subprocess.Popen(["dolphin"])
                return "Files opened."
            elif action == "open_vscode":
                subprocess.Popen(["code"])
                return "VS Code opened."
            
            # Close Apps
            elif action == "close_terminal":
                os.system("killall konsole")
                return "Terminal closed."
            elif action == "close_browser":
                os.system("killall firefox-esr") 
                return "Browser closed."
            elif action == "close_files":
                os.system("killall dolphin")
                return "Files closed."
            elif action == "close_vscode":
                os.system("killall code")
                return "VS Code closed."
            
            # Sensors
            elif action == "get_time":
                now = datetime.datetime.now()
                return now.strftime("It is %I:%M %p.")
            elif action == "check_status":
                cpu = psutil.cpu_percent()
                ram = psutil.virtual_memory().percent
                return f"CPU: {cpu}%, RAM: {ram}%."
            
            # Google Search
            elif action.startswith("search_google:"):
                query = action.replace("search_google:", "").strip()
                webbrowser.open(f"https://google.com/search?q={query}")
                return f"Searched Google for {query}."

            else:
                return f"Unknown command: {action}"

        except Exception as e:
            return f"Execution Error: {e}"