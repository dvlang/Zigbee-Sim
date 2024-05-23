#write a python language program to simulate a zigbee mesh network with multiple nodes that randomly exchange 
#frames over the course of a run. nodes should recieve all frames send by sender and forward frames not intended 
#for them. Ask the user to choose the number of nodes and the number of frames. Include CSMA/CE and binary exponential backoff. 
#Output a line showing each received frame. also output a line whenever a collision occurrs.

#
#0.1:  add a print when a node sends a frame
#0.2: update to use zigbee frame format
#0.3: when a node must backoff ensure that it re-attempts transmission

#################################################################################################################################################


import random
import time

#Represents each node in the network with added functionalities.
import random
import time

class Node:
    def __init__(self, node_id, network):
        self.node_id = node_id
        self.network = network
        self.received_frames = []

    def send_frame(self, dest_id, frame_id, payload, attempt=0):
        print(f"Node {self.node_id} is attempting to send frame {frame_id} to Node {dest_id} (Attempt {attempt + 1})")
        frame = ZigbeeFrame(self.node_id, dest_id, frame_id, payload)
        success = self.network.send_frame(frame)
        if not success:
            self.retry_frame(dest_id, frame_id, payload, attempt + 1)

    def retry_frame(self, dest_id, frame_id, payload, attempt):
        if attempt < self.network.max_retries:
            backoff_time = self.network.calculate_backoff(attempt)
            print(f"Node {self.node_id} backing off for {backoff_time:.3f} seconds (Attempt {attempt + 1})")
            time.sleep(backoff_time)
            self.send_frame(dest_id, frame_id, payload, attempt)
        else:
            print(f"Node {self.node_id} failed to send frame {frame_id} to Node {dest_id} after {attempt} attempts")

    def receive_frame(self, frame):
        self.received_frames.append(frame)
        print(f"Node {self.node_id} received frame {frame.frame_id} from Node {frame.source_id} with payload: {frame.payload}")

        if frame.dest_id != self.node_id:
            self.network.send_frame(frame)

class ZigbeeFrame:
    def __init__(self, source_id, dest_id, frame_id, payload):
        self.frame_type = 'data'  # Simplified for this simulation
        self.source_id = source_id
        self.dest_id = dest_id
        self.frame_id = frame_id
        self.payload = payload


#Manages nodes and frames, handles collisions, and forwards frames.
class Network:
    def __init__(self, num_nodes, max_retries=5):
        self.nodes = [Node(i, self) for i in range(num_nodes)]
        self.channel_busy = False
        self.collisions = 0
        self.max_retries = max_retries

    def send_frame(self, frame):
        if not self.is_channel_free():
            self.collisions += 1
            print(f"Collision occurred while sending frame {frame.frame_id} from Node {frame.source_id}")
            return False
        else:
            self.channel_busy = True
            print(f"Frame {frame.frame_id} sent from Node {frame.source_id} to Node {frame.dest_id} with payload: {frame.payload}")
            for node in self.nodes:
                if node.node_id != frame.source_id:
                    node.receive_frame(frame)
            self.channel_busy = False
            return True

    def is_channel_free(self):
        return not self.channel_busy

    def calculate_backoff(self, attempt):
        # Binary exponential backoff: 2^attempt * base_time
        base_time = 0.01
        return random.uniform(0, (2 ** attempt) * base_time)

    def start_simulation(self, num_frames):
        for _ in range(num_frames):
            sender_id = random.choice(range(len(self.nodes)))
            dest_id = random.choice(range(len(self.nodes)))
            while dest_id == sender_id:
                dest_id = random.choice(range(len(self.nodes)))
            frame_id = random.randint(1000, 9999)
            payload = f"Payload {frame_id}"
            self.nodes[sender_id].send_frame(dest_id, frame_id, payload)
            time.sleep(random.uniform(0.01, 0.1))
        print(f"Total collisions: {self.collisions}")

def main():
    num_nodes = int(input("Enter the number of nodes: "))
    num_frames = int(input("Enter the number of frames: "))
    network = Network(num_nodes)
    network.start_simulation(num_frames)

if __name__ == "__main__":
    main()
