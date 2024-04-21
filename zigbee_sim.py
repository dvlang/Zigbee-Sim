import random
import time

class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.backoff_exp = 0
        self.frame_to_send = None

    def generate_frame(self):
        return f"Frame from Node {self.node_id}"

    def send_frame(self):
        self.frame_to_send = self.generate_frame()

    def decrease_backoff(self):
        self.backoff_exp -= 1 if self.backoff_exp > 0 else 0

    def reset_backoff(self):
        self.backoff_exp = 0

def simulate_zigbee_network(num_nodes, num_frames):
    nodes = [Node(i) for i in range(num_nodes)]
    frames = [None] * num_nodes
    collisions = 0

    for _ in range(num_frames):
        # Each node attempts to send a frame
        for node in nodes:
            node.send_frame()

        # Check for collisions
        active_nodes = [node for node in nodes if node.frame_to_send is not None]
        if len(active_nodes) > 1:
            collisions += 1
            print("Collision occurred!")

            # Backoff mechanism
            for node in active_nodes:
                node.backoff_exp = random.randint(0, min(10, 2 ** node.backoff_exp + 1))

        # Wait for a random time before checking again
        time.sleep(0.5)

        # Nodes try to send frames again after backoff
        for node in nodes:
            if node.frame_to_send is not None:
                if node.backoff_exp == 0:
                    frames[node.node_id] = node.frame_to_send
                    node.frame_to_send = None
                else:
                    node.decrease_backoff()

    # Print received frames
    print("\nReceived Frames:")
    for i, frame in enumerate(frames):
        print(f"Node {i}: {frame}")

    print(f"\nTotal Collisions: {collisions}")

def main():
    num_nodes = int(input("Enter the number of nodes: "))
    num_frames = int(input("Enter the number of frames to exchange: "))
    simulate_zigbee_network(num_nodes, num_frames)

if __name__ == "__main__":
    main()
