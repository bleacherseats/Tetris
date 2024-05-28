# main_parallel.py
from dqn_agent import DQNAgent
from worker import worker
import multiprocessing as mp
import gym
import numpy as np

def main():
    num_workers = mp.cpu_count()  # Number of parallel workers
    env_name = "CartPole-v1"  # Replace with your environment
    state_size = gym.make(env_name).observation_space.shape[0]
    action_size = gym.make(env_name).action_space.n
    agent = DQNAgent(state_size, action_size)
    
    processes = []
    parent_conns = []

    for _ in range(num_workers):
        parent_conn, child_conn = mp.Pipe()
        p = mp.Process(target=worker, args=(agent, env_name, child_conn))
        processes.append(p)
        parent_conns.append(parent_conn)
        p.start()

    for parent_conn in parent_conns:
        total_reward = parent_conn.recv()
        print(f"Total Reward: {total_reward}")

    for p in processes:
        p.join()

    batch_size = 32
    if len(agent.memory) > batch_size:
        agent.replay(batch_size)

if __name__ == "__main__":
    main()
