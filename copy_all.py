import os

# List of directories to process
directories = ["chats", "conversa_dj"]
output_file = "output.txt"

with open(output_file, 'w') as file:
    for dir_name in directories:
        if os.path.isdir(dir_name):
            file.write(f"Directory: {dir_name}\n")
            for root, dirs, files in os.walk(dir_name):
                # Skip __pycache__ directories
                dirs[:] = [d for d in dirs if d != '__pycache__']

                # Write directory names
                for dir in dirs:
                    file.write(f"Subdirectory: {os.path.join(root, dir)}\n")

                # Write file names and contents
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    file.write(f"File: {file_path}\n")
                    try:
                        with open(file_path, 'r') as f:
                            content = f.read()
                        file.write(f"Contents:\n{content}\n")
                    except Exception as e:
                        file.write(f"Error reading file: {e}\n")
            file.write("\n")
        else:
            print(f"Directory not found: {dir_name}")

print(f"Content written to {output_file}")
