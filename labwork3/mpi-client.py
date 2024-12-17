from constant import Signal, BUFFERSIZE  # Ensure these constants are correctly defined in constant.py
from time import sleep
import os
from mpi4py import MPI

def send_signal(comm, signal, dest):
    """Send a signal to a specific destination."""
    comm.send(signal.value, dest=dest)

def recv_signal(comm, source) -> bytes:
    """Receive a signal from a specific source."""
    return comm.recv(source=source)

def send_file(comm, file_path, dest) -> None:
    """Send a file to the destination process."""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        comm.send(Signal.ERROR, dest=dest)
        return
    
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    print(f"Sending file: {file_name} ({file_size} bytes)")

    # Send file start signal and details
    comm.send(Signal.SEND_A_FILE, dest=dest)
    comm.send(file_name.encode(), dest=dest)  # Send file name
    comm.send(file_size, dest=dest)  # Send file size

    # Send file content
    with open(file_path, 'rb') as file:
        while chunk := file.read(BUFFERSIZE):
            comm.send(chunk, dest=dest)
        
    comm.send(Signal.DONE, dest=dest)
    print(f"File sent: {file_name}")

def request_file(comm, file_name, dest, save_file=None):
    """Request a file from the server."""
    if save_file is None:
        save_file = file_name

    send_signal(comm, Signal.REQUEST_A_FILE, dest)

    # Send file name
    comm.send(file_name.encode(), dest=dest)

    # Receive response
    response = recv_signal(comm, dest)
    if response == Signal.ERROR:
        print("Error: File not found")
        return

    # Save the file
    with open(save_file, 'wb') as file:
        while True:
            data = comm.recv(source=dest)

            if data == Signal.DONE:
                break

            file.write(data)

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    print(f"Client Rank: {rank}, Total Clients: {size}")

    SERVER_RANK = 0  # Assuming the server runs on rank 0

    try:
        # Uncomment desired operation
        send_file(comm, 'file-transfered/client-send/send0.txt', dest=SERVER_RANK)
        #request_file(comm, "send0.txt", SERVER_RANK)
    except Exception as e:
        print(f"Error: {e}")

    # Close the server
    send_signal(comm, Signal.CLOSE_SERVER, SERVER_RANK)
    MPI.Finalize()
