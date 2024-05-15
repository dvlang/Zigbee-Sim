import random

class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.backoff = 0
    
    def send_frame(self, frame):
        print(f"Node {self.node_id} sending frame: {frame}")
        return frame

    def receive_frame(self, frame):
        print(f"Node {self.node_id} received frame: {frame}")

def simulate_zigbee_network(num_nodes, num_frames):
    nodes = [Node(i) for i in range(num_nodes)]
    frames = [f"Frame {i}" for i in range(num_frames)]

    for frame in frames:
        transmitting_node = random.choice(nodes)
        transmitted_frame = transmitting_node.send_frame(frame)

        for node in nodes:
            if node != transmitting_node:
                if random.random() < 0.5:  # Probability of sensing the channel
                    print(f"Node {node.node_id} sensed the channel busy.")
                    if node.backoff == 0:
                        print(f"Node {node.node_id} starts the backoff process.")
                    while node.backoff > 0:
                        print(f"Node {node.node_id} backoff: {node.backoff}")
                        node.backoff -= 1
                        if random.random() < 0.5:  # Probability of collision
                            print(f"Collision occurred at Node {node.node_id}")
                            node.backoff = min(node.backoff + 1, 7)  # Binary exponential backoff
                            break
                    else:
                        node.receive_frame(transmitted_frame)
                        node.backoff = 0

if __name__ == "__main__":
    num_nodes = int(input("Enter the number of nodes: "))
    num_frames = int(input("Enter the number of frames: "))
    simulate_zigbee_network(num_nodes, num_frames)