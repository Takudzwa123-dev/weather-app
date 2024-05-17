#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import mysql.connector
import re
import os
import tkinter as tk
from tkinter import messagebox

# MySQL database configuration
db_config = {
    'user': 'root',
    'password': 'Taku@12345',
    'host': 'localhost',
    'database': 'ipam_db'
}

# Function to establish MySQL connection with retry logic
def establish_connection():
    attempt = 1
    max_attempts = 3
    while attempt <= max_attempts:
        try:
            db_conn = mysql.connector.connect(**db_config)
            db_cursor = db_conn.cursor()
            return db_conn, db_cursor
        except mysql.connector.Error as e:
            print(f"Attempt {attempt}: {e}")
            if attempt == max_attempts:
                print("Failed to connect to TK-IPAM Solution !!!. Exiting.")
                exit_program()
            print("Retrying connection...")
            attempt += 1

# Initialize MySQL connection
db_conn, db_cursor = establish_connection()

# Function to create a new IP address entry
def create_ip_address(ip_address, prefix_length, status, hostname, requester, date_requested):
    query = "INSERT INTO ipam_table (ip_address, prefix_length, status, hostname, requester, date_requested) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (ip_address, prefix_length, status, hostname, requester, date_requested)
    db_cursor.execute(query, values)
    db_conn.commit()

# Function to read IP addresses with search functionality
def read_ip_addresses(search_query=None):
    if search_query:
        query = "SELECT * FROM ipam_table WHERE ip_address LIKE %s OR requester LIKE %s OR hostname LIKE %s"
        values = (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%")
        db_cursor.execute(query, values)
    else:
        query = "SELECT * FROM ipam_table"
        db_cursor.execute(query)
    return db_cursor.fetchall()

# Function to update an IP address
def update_ip_address(ip_address, hostname, requester, status, date_requested):
    query = "UPDATE ipam_table SET hostname = %s, requester = %s, status = %s, date_requested = %s WHERE ip_address = %s"
    values = (hostname, requester, status, date_requested, ip_address)
    db_cursor.execute(query, values)
    db_conn.commit()

# Function to delete an IP address
def delete_ip_address(ip_address):
    query = "DELETE FROM ipam_table WHERE ip_address = %s"
    values = (ip_address,)
    db_cursor.execute(query, values)
    db_conn.commit()

# Function to create a new GUI window
def create_window():
    window = tk.Tk()
    window.title("IP Address Management System")
    window.geometry("600x400")

    # Function to handle create IP address button click
    def create_ip_address_click():
        ip = ip_entry.get()
        prefix_length = int(prefix_length_entry.get())
        status = status_var.get()
        hostname = hostname_entry.get()
        requester = requester_entry.get()
        date_requested = date_requested_entry.get()
        create_ip_address(ip, prefix_length, status, hostname, requester, date_requested)
        messagebox.showinfo("Success", "IP address created successfully.")

    # Function to handle search button click
    def search_click():
        search_query = search_entry.get()
        ip_addresses = read_ip_addresses(search_query)
        display_ip_addresses(ip_addresses)

    # Function to display IP addresses
    def display_ip_addresses(ip_addresses):
        result_text.delete("1.0", tk.END)
        if ip_addresses:
            for ip_address in ip_addresses:
                result_text.insert(tk.END, f"IP Address: {ip_address[1]}\n")
                result_text.insert(tk.END, f"Prefix Length: {ip_address[2]}\n")
                result_text.insert(tk.END, f"Status: {ip_address[3]}\n")
                result_text.insert(tk.END, f"Hostname: {ip_address[4]}\n")
                result_text.insert(tk.END, f"Requester: {ip_address[5]}\n")
                result_text.insert(tk.END, f"Date Requested: {ip_address[6]}\n")
                result_text.insert(tk.END, "-----------------------------\n")
        else:
            result_text.insert(tk.END, "No matching IP addresses found.")

    # Function to handle update button click
    def update_click():
        ip = update_ip_entry.get()
        hostname = update_hostname_entry.get()
        requester = update_requester_entry.get()
        status = update_status_var.get()
        date_requested = update_date_requested_entry.get()
        update_ip_address(ip, hostname, requester, status, date_requested)
        messagebox.showinfo("Success", "IP address updated successfully.")

    # Function to handle delete button click
    def delete_click():
        ip = delete_ip_entry.get()
        delete_ip_address(ip)
        messagebox.showinfo("Success", "IP address deleted successfully.")

    # GUI elements for create IP address
    ip_label = tk.Label(window, text="IP Address:")
    ip_label.grid(row=0, column=0, padx=5, pady=5)
    ip_entry = tk.Entry(window)
    ip_entry.grid(row=0, column=1, padx=5, pady=5)

    prefix_length_label = tk.Label(window, text="Prefix Length:")
    prefix_length_label.grid(row=1, column=0, padx=5, pady=5)
    prefix_length_entry = tk.Entry(window)
    prefix_length_entry.grid(row=1, column=1, padx=5, pady=5)

    status_label = tk.Label(window, text="Status:")
    status_label.grid(row=2, column=0, padx=5, pady=5)
    status_var = tk.StringVar(window)
    status_var.set("unassigned")
    status_option = tk.OptionMenu(window, status_var, "assigned", "unassigned")
    status_option.grid(row=2, column=1, padx=5, pady=5)

    hostname_label = tk.Label(window, text="Hostname:")
    hostname_label.grid(row=3, column=0, padx=5, pady=5)
    hostname_entry = tk.Entry(window)
    hostname_entry.grid(row=3, column=1, padx=5, pady=5)

    requester_label = tk.Label(window, text="Requester:")
    requester_label.grid(row=4, column=0, padx=5, pady=5)
    requester_entry = tk.Entry(window)
    requester_entry.grid(row=4, column=1, padx=5, pady=5)

    date_requested_label = tk.Label(window, text="Date Requested:")
    date_requested_label.grid(row=5, column=0, padx=5, pady=5)
    date_requested_entry = tk.Entry(window)
    date_requested_entry.grid(row=5, column=1, padx=5, pady=5)

    create_button = tk.Button(window, text="Create IP Address", command=create_ip_address_click)
    create_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

    # GUI elements for read IP addresses
    search_label = tk.Label(window, text="Search:")
    search_label.grid(row=7, column=0, padx=5, pady=5)
    search_entry = tk.Entry(window)
    search_entry.grid(row=7, column=1, padx=5, pady=5)

    search_button = tk.Button(window, text="Search", command=search_click)
    search_button.grid(row=7, column=2, padx=5, pady=5)

    result_text = tk.Text(window, height=10, width=50)
    result_text.grid(row=8, column=0, columnspan=3, padx=5, pady=5)

    # GUI elements for update IP address
    update_ip_label = tk.Label(window, text="IP Address:")
    update_ip_label.grid(row=9, column=0, padx=5, pady=5)
    update_ip_entry = tk.Entry(window)
    update_ip_entry.grid(row=9, column=1, padx=5, pady=5)

    update_hostname_label = tk.Label(window, text="Hostname:")
    update_hostname_label.grid(row=10, column=0, padx=5, pady=5)
    update_hostname_entry = tk.Entry(window)
    update_hostname_entry.grid(row=10, column=1, padx=5, pady=5)

    update_requester_label = tk.Label(window, text="Requester:")
    update_requester_label.grid(row=11, column=0, padx=5, pady=5)
    update_requester_entry = tk.Entry(window)
    update_requester_entry.grid(row=11, column=1, padx=5, pady=5)

    update_status_label = tk.Label(window, text="Status:")
    update_status_label.grid(row=12, column=0, padx=5, pady=5)
    update_status_var = tk.StringVar(window)
    update_status_var.set("unassigned")
    update_status_option = tk.OptionMenu(window, update_status_var, "assigned", "unassigned")
    update_status_option.grid(row=12, column=1, padx=5, pady=5)

    update_date_requested_label = tk.Label(window, text="Date Requested:")
    update_date_requested_label.grid(row=13, column=0, padx=5, pady=5)
    update_date_requested_entry = tk.Entry(window)
    update_date_requested_entry.grid(row=13, column=1, padx=5, pady=5)

    update_button = tk.Button(window, text="Update IP Address", command=update_click)
    update_button.grid(row=14, column=0, columnspan=2, padx=5, pady=5)

    # GUI elements for delete IP address
    delete_ip_label = tk.Label(window, text="IP Address:")
    delete_ip_label.grid(row=15, column=0, padx=5, pady=5)
    delete_ip_entry = tk.Entry(window)
    delete_ip_entry.grid(row=15, column=1, padx=5, pady=5)

    delete_button = tk.Button(window, text="Delete IP Address", command=delete_click)
    delete_button.grid(row=16, column=0, columnspan=2, padx=5, pady=5)

    window.mainloop()

# Start the program
create_window()

