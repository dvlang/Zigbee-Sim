#run_14
#update such that if a message received by a node is not addressed to it, it is forwarded
import random
import string
import time

# Constants defined by the 802.15.4 Zigbee CSMA-CA standard
SYMBOL_DURATION = 16 * (10 ** -6)  # Duration of one symbol (in seconds)
SLOT_DURATION = 20 * SYMBOL_DURATION  # Duration of one slot (in seconds)

class ZigbeeFrame:
    def __init__(self, src_node, dst_node, payload, timestamp=None):
        self.src_node = src_node
        self.dst_node = dst_node
        self.payload = payload
        self.timestamp = timestamp if timestamp is not None else time.time()

    def __str__(self):
        return f"ZigbeeFrame(src_node={self.src_node}, dst_node={self.dst_node}, payload={self.payload}, timestamp={self.timestamp})"


class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.node_number = node_id
        self.backoff = 0
        self.collision = False
    
    def send_frame(self, frame, nodes):
        frame.timestamp = time.time()
        print(f"Node {self.node_id} sending frame at time {frame.timestamp}: {frame}")
        time.sleep(0.0048)  # Introduce a delay to simulate frame transmission time
        for node in nodes:
            if node.node_number == frame.dst_node:
                node.receive_frame(frame, nodes)
                break

    def receive_frame(self, frame, nodes):
        frame.timestamp = time.time()
        print(f"Node {self.node_id} received frame at time {frame.timestamp}: {frame}")
        if frame.dst_node != self.node_number:
            print("Not for me, forwarding the message")
            # Forward the message
            self.send_frame(frame, nodes)
        else:
            print("Message is for me")

def generate_random_payload():
    alphanumeric_chars = string.ascii_letters + string.digits
    return ''.join(random.choice(alphanumeric_chars) for _ in range(104)).encode('utf-8')  # Generate a random alphanumeric string of length 104 bytes

def simulate_zigbee_network(num_nodes, num_frames):
    nodes = [Node(i) for i in range(num_nodes)]

    for _ in range(num_frames):
        # Simulate channel sensing
        channel_busy = any(node.backoff > 0 for node in nodes)

        if not channel_busy:
            transmitting_node = random.choice(nodes)
            destination_node = random.choice(nodes)  # Allow frames to be sent to any node

            payload = generate_random_payload()

            frame = ZigbeeFrame(transmitting_node.node_number, destination_node.node_number, payload)

            if transmitting_node.collision:
                print(f"Collision occurred at Node {transmitting_node.node_id}")
                transmitting_node.backoff = random.randint(0, 2 ** transmitting_node.backoff - 1)
                backoff_symbols = min(transmitting_node.backoff, 5)  # Ensure backoff does not exceed maximum allowed value (5 symbols)
                backoff_time = backoff_symbols * SLOT_DURATION
                print(f"Node {transmitting_node.node_id} starts the backoff process for {backoff_symbols} symbols ({backoff_time} seconds).")
                transmitting_node.collision = False
            else:
                transmitting_node.send_frame(frame, nodes)

        for node in nodes:
            if node != transmitting_node:
                if node.backoff == 0:
                    print(f"Node {node.node_id} starts the backoff process for {node.backoff} symbols ({node.backoff * SLOT_DURATION} seconds).")
                while node.backoff > 0:
                    print(f"Node {node.node_id} backoff: {node.backoff}")
                    time.sleep(SLOT_DURATION)  # Simulate time for backoff
                    node.backoff -= 1

                    # After backoff, check if channel is still busy
                    channel_busy = any(other_node.backoff > 0 for other_node in nodes if other_node != node)
                    if channel_busy:
                        break

        time.sleep(0.0048)  # Introduce a delay to simulate frame transmission time

if __name__ == "__main__":
    num_nodes = int(input("Enter the number of nodes: "))
    num_frames = int(input("Enter the number of frames: "))
    simulate_zigbee_network(num_nodes, num_frames)
