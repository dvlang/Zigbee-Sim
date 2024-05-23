#run_15
#update program so that multiple nodes randomly attempt to transmit at same time
import random
import string
import time
from threading import Thread, Lock

# Constants defined by the 802.15.4 Zigbee CSMA-CA standard
SYMBOL_DURATION = 16 * (10 ** -6)  # Duration of one symbol (in seconds)
SLOT_DURATION = 20 * SYMBOL_DURATION  # Duration of one slot (in seconds)
FRAME_TRANSMISSION_TIME = 0.0048  # Time to transmit a frame (in seconds)
BACKOFF_EXPONENT = 5  # Maximum value of the backoff exponent

lock = Lock()  # A lock to manage concurrent access to the medium

class ZigbeeFrame:
    def __init__(self, src_node, dst_node, payload, timestamp=None):
        self.src_node = src_node
        self.dst_node = dst_node
        self.payload = payload
        self.timestamp = timestamp if timestamp is not None else time.time()

    def __str__(self):
        return f"ZigbeeFrame(src_node={self.src_node}, dst_node={self.dst_node}, payload={self.payload}, timestamp={self.timestamp})"

class Node:
    def __init__(self, node_id, nodes):
        self.node_id = node_id
        self.node_number = node_id
        self.backoff = 0
        self.collision = False
        self.nodes = nodes

    def generate_random_payload(self):
        alphanumeric_chars = string.ascii_letters + string.digits
        return ''.join(random.choice(alphanumeric_chars) for _ in range(104)).encode('utf-8')  # Generate a random alphanumeric string of length 104 bytes

    def send_frame(self):
        while True:
            # Randomly decide if the node will attempt to transmit
            time.sleep(random.uniform(0.1, 1.0))  # Random delay before attempting to send

            destination_node = random.choice(self.nodes)
            if destination_node.node_number == self.node_number:
                continue  # Do not send to itself

            payload = self.generate_random_payload()
            frame = ZigbeeFrame(self.node_number, destination_node.node_number, payload)

            attempt_success = False
            while not attempt_success:
                with lock:
                    # Simulate channel sensing
                    if any(node.collision for node in self.nodes):
                        self.collision = True
                    else:
                        print(f"Node {self.node_id} sending frame at time {time.time()}: {frame}")
                        time.sleep(FRAME_TRANSMISSION_TIME)  # Simulate frame transmission time
                        destination_node.receive_frame(frame, self.nodes)
                        self.collision = False
                        attempt_success = True

                if self.collision:
                    print(f"Collision occurred at Node {self.node_id}")
                    self.backoff = random.randint(0, 2 ** min(self.backoff, BACKOFF_EXPONENT) - 1)
                    backoff_time = self.backoff * SLOT_DURATION
                    print(f"Node {self.node_id} starts the backoff process for {self.backoff} slots ({backoff_time} seconds).")
                    time.sleep(backoff_time)
                    self.backoff += 1
                else:
                    self.backoff = 0

    def receive_frame(self, frame, nodes):
        frame.timestamp = time.time()
        print(f"Node {self.node_id} received frame at time {frame.timestamp}: {frame}")
        if frame.dst_node != self.node_number:
            print("Not for me, forwarding the message")
            self.send_frame()

def simulate_zigbee_network(num_nodes, num_frames):
    nodes = [Node(i, None) for i in range(num_nodes)]
    for node in nodes:
        node.nodes = nodes  # Assign the list of nodes to each node

    threads = []
    for node in nodes:
        thread = Thread(target=node.send_frame)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    num_nodes = int(input("Enter the number of nodes: "))
    num_frames = int(input("Enter the number of frames: "))  # This parameter is no longer needed but kept for compatibility
    simulate_zigbee_network(num_nodes, num_frames)
