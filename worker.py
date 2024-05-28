# worker.py
import numpy as np
import random
import gym

def worker(agent, env_name, conn):
    env = gym.make(env_name)
    state = env.reset()
    total_reward = 0
    done = False

    while not done:
        state = np.reshape(state, [1, agent.state_size])
        action = agent.act(state)
        next_state, reward, done, _ = env.step(action)
        total_reward += reward
        next_state = np.reshape(next_state, [1, agent.state_size])
        agent.remember(state, action, reward, next_state, done)
        state = next_state

        if done:
            conn.send(total_reward)
            conn.close()
            break
