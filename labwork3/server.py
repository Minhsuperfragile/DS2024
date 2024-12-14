from mpi4py import MPI
import os

# Constants
BUFFERSIZE = 1024  # Adjust this based on your needs

def receive_signal(comm):
    """Receive signal using MPI"""
    signal = comm.recv(source=0, tag=11)
    print(f"Server: Received signal: {signal}")
    return signal

def receive_file(comm):
    """Receive a file from client using MPI"""
    # Receive the signal indicating that the client is sending a file
    signal = receive_signal(comm)
    if signal != 'SEND_FILE':
        print("Server: Unexpected signal")
        return

    # Receive the file name
    file_name = comm.recv(source=0, tag=12)
    print(f"Server: Receiving file: {file_name}")

    # Open the file for writing
    with open(f"received_{file_name}", 'wb') as f:
        while True:
            # Receive file data in chunks
            data = bytearray(BUFFERSIZE)
            status = comm.Recv([data, MPI.BYTE], source=0, tag=13)

            if status.Get_elements(MPI.BYTE) == 0:  # No data, file transmission is complete
                break

            f.write(data)
            print(f"Server: Received chunk of size {len(data)} bytes.")

    print(f"Server: File {file_name} received successfully.")

def main():
    """Main function for the MPI server."""
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if rank == 1:  # Server logic (rank 1)
        print("Server is running...")
        # Receive the file
        receive_file(comm)

if __name__ == "__main__":
    main()
