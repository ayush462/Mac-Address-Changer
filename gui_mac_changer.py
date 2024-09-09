import subprocess
import re
import tkinter as tk
from tkinter import messagebox


def mac_changer(interface, new_mac):
    print(f"[+] Changing MAC address for {interface} to {new_mac}")
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    try:
        ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode('utf-8')
        mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
        if mac_address_search_result:
            return mac_address_search_result.group(0)
        else:
            return None
    except subprocess.CalledProcessError:
        return None


def change_mac():
    interface = interface_entry.get()
    new_mac = mac_entry.get()

    if not interface:
        messagebox.showerror("Input Error", "Please specify the interface.")
        return

    if not new_mac:
        messagebox.showerror("Input Error", "Please specify the new MAC address.")
        return

    current_mac = get_current_mac(interface)
    if current_mac:
        print(f"[+] Current MAC is {current_mac}")
        mac_changer(interface, new_mac)
        current_mac = get_current_mac(interface)

        if current_mac == new_mac:
            messagebox.showinfo("Success", f"MAC address successfully changed to {new_mac}")
        else:
            messagebox.showerror("Failure", "Failed to change MAC address.")
    else:
        messagebox.showerror("Error", "Could not find MAC address for the specified interface.")



window = tk.Tk()
window.title("MAC Address Changer")


interface_label = tk.Label(window, text="Interface")
interface_label.pack()

interface_entry = tk.Entry(window)
interface_entry.pack()


mac_label = tk.Label(window, text="New MAC Address")
mac_label.pack()

mac_entry = tk.Entry(window)
mac_entry.pack()


change_button = tk.Button(window, text="Change MAC Address", command=change_mac)
change_button.pack()


window.mainloop()
