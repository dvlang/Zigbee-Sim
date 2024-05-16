#run_10
#if a node receives a message that is not for its address, print "not for me" and resend that message. if a node receives a message for it's address print "message is for me". 
import random
import string
import time

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
                node.receive_frame(frame)
                break

    def receive_frame(self, frame):
        frame.timestamp = time.time()
        print(f"Node {self.node_id} received frame at time {frame.timestamp}: {frame}")
        if frame.dst_node != self.node_number:
            print("Not for me")
            # Resend the message
            frame.src_node, frame.dst_node = frame.dst_node, frame.src_node  # Swap source and destination nodes
            self.send_frame(frame, [])
        else:
            print("Message is for me")

def generate_random_payload():
    alphanumeric_chars = string.ascii_letters + string.digits
    return ''.join(random.choice(alphanumeric_chars) for _ in range(104)).encode('utf-8')  # Generate a random alphanumeric string of length 104 bytes

def simulate_zigbee_network(num_nodes, num_frames):
    nodes = [Node(i) for i in range(num_nodes)]

    for _ in range(num_frames):
        transmitting_node = random.choice(nodes)
        destination_node = random.choice(nodes)  # Allow frames to be sent to any node

        payload = generate_random_payload()

        frame = ZigbeeFrame(transmitting_node.node_number, destination_node.node_number, payload)

        if transmitting_node.collision:
            print(f"Collision occurred at Node {transmitting_node.node_id}")
            transmitting_node.backoff = random.randint(0, 2 ** transmitting_node.backoff - 1)
            transmitting_node.collision = False
        else:
            transmitting_node.send_frame(frame, nodes)

        for node in nodes:
            if node != transmitting_node:
                if random.random() < 0.5:  # Probability of sensing the channel busy
                    print(f"Node {node.node_id} sensed the channel busy.")
                    if node.backoff == 0:
                        print(f"Node {node.node_id} starts the backoff process.")
                    while node.backoff > 0:
                        print(f"Node {node.node_id} backoff: {node.backoff}")
                        time.sleep(0.5)  # Simulate time for backoff
                        node.backoff -= 1
                        if random.random() < 0.5:  # Probability of collision
                            print(f"Collision occurred at Node {node.node_id}")
                            node.collision = True
                            node.backoff = min(node.backoff + 1, 5)  # Binary exponential backoff
                            break
                    else:
                        node.backoff = 0

if __name__ == "__main__":
    num_nodes = int(input("Enter the number of nodes: "))
    num_frames = int(input("Enter the number of frames: "))
    simulate_zigbee_network(num_nodes, num_frames)
