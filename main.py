def log_console(text):
    print(text)


def log_file(text, filepath='log.txt'):
    with open(filepath, 'w') as f:
        f.write(text)


target = 'Hello, World!'
log_console(target)
log_file(target)
