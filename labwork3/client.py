from mpi4py import MPI
import os
import time

# Constants
BUFFERSIZE = 1024  # Adjust this based on your needs

def send_signal(comm, signal):
    """Send signal using MPI"""
    print(f"Client: Sending signal: {signal}")
    comm.send(signal, dest=1, tag=11)

def receive_signal(comm):
    """Receive signal using MPI"""
    signal = comm.recv(source=1, tag=11)
    print(f"Client: Received signal: {signal}")
    return signal

def send_file(comm, file_name):
    """Send a file to server using MPI"""
    if not os.path.exists(file_name):
        raise FileNotFoundError(f"{file_name} does not exist.")

    # Send a signal that we are about to send a file
    send_signal(comm, 'SEND_FILE')

    # Send the file name to the server
    file_name = file_name.split("/")[-1]  # Send only the file name, not the full path
    comm.send(file_name, dest=1, tag=12)
    print(f"Client: Sent file name: {file_name}")

    # Send the file in chunks
    with open(file_name, 'rb') as f:
        while chunk := f.read(BUFFERSIZE):
            comm.Send([chunk, MPI.BYTE], dest=1, tag=13)  # Send file data
            print(f"Client: Sent chunk of size {len(chunk)} bytes.")

    # Send a 'done' signal when file is completely sent
    send_signal(comm, 'DONE')

def main():
    """Main function for the MPI client."""
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if rank == 0:  # Client logic (rank 0)
        print("Client is running...")
        file_to_send = '/home/hungday/Documents/python/DS2024/labwork3/send0.txt'  # Example file to send

        # Send the file
        send_file(comm, file_to_send)

if __name__ == "__main__":
    main()
