# import the tkinter library as tk
import tkinter as tk

# define the encryption function that takes a message and a key and returns the encrypted message
def encrypt(message, key):
    # initialize an empty string for the encrypted message and set m to 26 (the number of letters in the alphabet)
    encrypted_message = ""
    m = 26
    # iterate through each character in the message
    for char in message:
        # check if the character is a letter
        if char.isalpha():
            # if the character is uppercase, set p to the ASCII value of the character minus the ASCII value of A
            if char.isupper():
                p = ord(char) - ord('A')
                # apply the Caesar cipher encryption formula to the character and add the result to the encrypted message
                encrypted_char = chr((p + key) % m + ord('A'))
            else:
                # if the character is lowercase, set p to the ASCII value of the character minus the ASCII value of a
                p = ord(char) - ord('a')
                # apply the Caesar cipher encryption formula to the character and add the result to the encrypted message
                encrypted_char = chr((p + key) % m + ord('a'))
            encrypted_message += encrypted_char
        else:
            # if the character is not a letter, add it to the encrypted message as is
            encrypted_message += char
    return encrypted_message

# define the decryption function that takes an encrypted message and a key and returns the decrypted message
def decrypt(message, key):
    # initialize an empty string for the decrypted message and set m to 26 (the number of letters in the alphabet)
    decrypted_message = ""
    m = 26
    # iterate through each character in the message
    for char in message:
        # check if the character is a letter
        if char.isalpha():
            # if the character is uppercase, set p to the ASCII value of the character minus the ASCII value of A
            if char.isupper():
                p = ord(char) - ord('A')
                # apply the Caesar cipher decryption formula to the character and add the result to the decrypted message
                decrypted_char = chr((p - key) % m + ord('A'))
            else:
                # if the character is lowercase, set p to the ASCII value of the character minus the ASCII value of a
                p = ord(char) - ord('a')
                # apply the Caesar cipher decryption formula to the character and add the result to the decrypted message
                decrypted_char = chr((p - key) % m + ord('a'))
            decrypted_message += decrypted_char
        else:
            # if the character is not a letter, add it to the decrypted message as is
            decrypted_message += char
    return decrypted_message

# define the function that encrypts the message entered by user1 and displays it for user2
def user1_encrypt_message():
    # get the message entered by user1 and strip any leading or trailing whitespace
    message = user1_input_text.get("1.0", tk.END).strip()
    # encrypt the message using the shared key
    encrypted_message = encrypt(message, shared_key)
    # clear the input text box for user2 and insert the encrypted message
    user2_input_text.delete("1.0", tk.END)
    user2_input_text.insert(tk.END, encrypted_message)
    # clear the input text box for user1
    user1_input_text.delete("1.0", tk.END)

# define the function that decrypts the message entered by user1 and displays it for user1
def user1_decrypt_message():
    # get the message entered by user1 and strip any leading or trailing whitespace
    message = user1_input_text.get("1.0", tk.END).strip()
    # decrypt the message using the shared key
    decrypted_message = decrypt(message, shared_key)
    # clear the output text box for user1 and insert the decrypted message
    user1_output_text.delete("1.0", tk.END)
    user1_output_text.insert(tk.END, decrypted_message)
    # clear the input text box for user1
    user1_input_text.delete("1.0", tk.END)

# define the function that decrypts the message entered by user2 and displays it for user2
def user2_decrypt_message():
    # get the message entered by user2 and strip any leading or trailing whitespace
    message = user2_input_text.get("1.0", tk.END).strip()
    # decrypt the message using the shared key
    decrypted_message = decrypt(message, shared_key)
    # clear the output text box for user2 and insert the decrypted message
    user2_output_text.delete("1.0", tk.END)
    user2_output_text.insert(tk.END, decrypted_message)
    # clear the input text box for user2
    user2_input_text.delete("1.0", tk.END)

# define the function that encrypts the message entered by user2 and displays it for user1
def user2_encrypt_message():
    # get the message entered by user2 and strip any leading or trailing whitespace
    message = user2_input_text.get("1.0", tk.END).strip()
    # encrypt the message using the shared key
    encrypted_message = encrypt(message, shared_key)
    # clear the input text box for user1 and insert the encrypted message
    user1_input_text.delete("1.0", tk.END)
    user1_input_text.insert(tk.END, encrypted_message)
    # clear the input text box for user2
    user2_input_text.delete("1.0", tk.END)

# GUI setup
root = tk.Tk()  # create the main window object
root.title("Encryption and Decryption")  # set the window title
root.configure(bg='purple')  # set the background color of the window

user1_frame = tk.Frame(root, bg='purple')
user1_frame.pack(side=tk.LEFT, padx=10, pady=10)

user2_frame = tk.Frame(root, bg='purple')
user2_frame.pack(side=tk.RIGHT, padx=10, pady=10)

# User 1 interface
user1_input_label = tk.Label(user1_frame, text="User 1 - Enter your message:", bg='purple', fg='white')
user1_input_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

user1_input_text = tk.Text(user1_frame, height=10, width=40)
user1_input_text.grid(row=1, column=0, padx=5, pady=5)

user1_encrypt_button = tk.Button(user1_frame, text="User 1 Encrypt", command=user1_encrypt_message, bg='yellow')
user1_encrypt_button.grid(row=2, column=0, padx=5, pady=5, sticky='w')

user1_decrypt_button = tk.Button(user1_frame, text="User 1 Decrypt", command=user1_decrypt_message, bg='yellow')
user1_decrypt_button.grid(row=3, column=0, padx=5, pady=5, sticky='w')

user1_output_label = tk.Label(user1_frame, text="User 1 - Decrypted:", bg='purple', fg='white')
user1_output_label.grid(row=4, column=0, padx=5, pady=5, sticky='w')

user1_output_text = tk.Text(user1_frame, height=10, width=40)
user1_output_text.grid(row=5, column=0, padx=5, pady=5)

# User 2 interface
user2_input_label = tk.Label(user2_frame, text="User 2 - Enter your message:", bg='purple', fg='white')
user2_input_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

user2_input_text = tk.Text(user2_frame, height=10, width=40)
user2_input_text.grid(row=1, column=0, padx=5, pady=5)

user2_decrypt_button = tk.Button(user2_frame, text="User 2 Decrypt", command=user2_decrypt_message, bg='yellow')
user2_decrypt_button.grid(row=2, column=0, padx=5, pady=5, sticky='w')

user2_encrypt_button = tk.Button(user2_frame, text="User 2 Encrypt", command=user2_encrypt_message, bg='yellow')
user2_encrypt_button.grid(row=3, column=0, padx=5, pady=5, sticky='w')

user2_output_label = tk.Label(user2_frame, text="User 2 - Decrypted:", bg='purple', fg='white')
user2_output_label.grid(row=4, column=0, padx=5, pady=5, sticky='w')

user2_output_text = tk.Text(user2_frame, height=10, width=40)
user2_output_text.grid(row=5, column=0, padx=5, pady=5)

# Key setup
shared_key = 11  # Shared key between users

root.mainloop()
