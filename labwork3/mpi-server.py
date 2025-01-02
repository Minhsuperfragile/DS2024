from mpi4py import MPI
import os

def download(fileName):

    if (os.path.exists(f"labwork3/receive/{fileName}")):
        with open(f"labwork3/receive/{fileName}", 'rb') as f:
            content = f.read()
        return content    
    else:
        return False

def upload(arguments):
    content, fileName = arguments
    with open(f"labwork3/receive/{fileName}", "wb") as f:
        f.write(content)
    return "Successfully"

def list(arguments):
    fileList = os.listdir("labwork3/receive")
    return fileList

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    print("Start the server")
    if rank == 0:
        options = {
                "UPLOAD": upload,
                "DOWNLOAD": download,
                "LIST": list,
            }

        while True:
            content = comm.recv(source=MPI.ANY_SOURCE)
            operation = content.get("operation")
            argument = content.get("argument")
            rank = content.get("rank")
            print(f"Receiving command from client {rank}: {operation}")

            if operation == "QUIT":
                print(f"Client {rank} log out.")

            if operation not in options:
                print("Invalid operation")
                continue
            else:
                response = options[operation](argument)
                print("Sending back")
                comm.send(response, dest=rank)

if __name__ == "__main__":
    main()