#write a python language program to simulate a zigbee mesh network with multiple nodes that randomly exchange 
#frames over the course of a run. nodes should recieve all frames send by sender and forward frames not intended 
#for them. Ask the user to choose the number of nodes and the number of frames. Include CSMA/CE and binary exponential backoff. 
#Output a line showing each received frame. also output a line whenever a collision occurrs.
import random
import time

class Node:
    def __init__(self, node_id, network):
        self.node_id = node_id
        self.network = network
        self.received_frames = []

    def send_frame(self, dest_id, frame_id):
        frame = Frame(self.node_id, dest_id, frame_id)
        self.network.send_frame(frame)

    def receive_frame(self, frame):
        self.received_frames.append(frame)
        print(f"Node {self.node_id} received frame {frame.frame_id} from Node {frame.source_id}")

        if frame.dest_id != self.node_id:
            self.network.send_frame(frame)

    def check_channel(self):
        return self.network.is_channel_free()

class Frame:
    def __init__(self, source_id, dest_id, frame_id):
        self.source_id = source_id
        self.dest_id = dest_id
        self.frame_id = frame_id

class Network:
    def __init__(self, num_nodes):
        self.nodes = [Node(i, self) for i in range(num_nodes)]
        self.channel_busy = False
        self.collisions = 0

    def send_frame(self, frame):
        if not self.is_channel_free():
            self.collisions += 1
            print(f"Collision occurred while sending frame {frame.frame_id} from Node {frame.source_id}")
            self.handle_collision()
        else:
            self.channel_busy = True
            for node in self.nodes:
                if node.node_id != frame.source_id:
                    node.receive_frame(frame)
            self.channel_busy = False

    def is_channel_free(self):
        return not self.channel_busy

    def handle_collision(self):
        time.sleep(random.uniform(0.001, 0.01))

    def start_simulation(self, num_frames):
        for _ in range(num_frames):
            sender_id = random.choice(range(len(self.nodes)))
            dest_id = random.choice(range(len(self.nodes)))
            while dest_id == sender_id:
                dest_id = random.choice(range(len(self.nodes)))
            frame_id = random.randint(1000, 9999)
            self.nodes[sender_id].send_frame(dest_id, frame_id)
            time.sleep(random.uniform(0.01, 0.1))
        print(f"Total collisions: {self.collisions}")

def main():
    num_nodes = int(input("Enter the number of nodes: "))
    num_frames = int(input("Enter the number of frames: "))
    network = Network(num_nodes)
    network.start_simulation(num_frames)

if __name__ == "__main__":
    main()