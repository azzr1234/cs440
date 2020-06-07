import gym
import numpy as np
import torch
from torch import nn
import utils
from policies import QPolicy


def make_dqn(statesize, actionsize):
    """
    Create a nn.Module instance for the q leanring model.

    @param statesize: dimension of the input continuous state space.
    @param actionsize: dimension of the descrete action space.

    @return model: nn.Module instance
    """
    model=nn.Sequential(
            nn.Linear(statesize,256),
            nn.ReLU(),
            nn.Linear(256,actionsize)
            )
    return model


class DQNPolicy(QPolicy):
    """
    Function approximation via a deep network
    """

    def __init__(self, model, statesize, actionsize, lr, gamma):
        """
        Inititalize the dqn policy

        @param model: the nn.Module instance returned by make_dqn
        @param statesize: dimension of the input continuous state space.
        @param actionsize: dimension of the descrete action space.
        @param lr: learning rate 
        @param gamma: discount factor
        """
        super().__init__(statesize, actionsize, lr, gamma)
        self.optimizer=torch.optim.Adam(model.parameters(),lr=lr)
        self.lossfun=nn.SmoothL1Loss(reduce=False, size_average=False)
        self.model=model

    def qvals(self, state):
        """
        Returns the q values for the states.

        @param state: the state
        
        @return qvals: the q values for the state for each action. 
        """
        self.model.eval()
        with torch.no_grad():
            states = torch.from_numpy(state).type(torch.FloatTensor)
            qvals = self.model(states)
        return qvals.numpy()

    def td_step(self, state, action, reward, next_state, done):
        """
        One step TD update to the model

        @param state: the current state
        @param action: the action
        @param reward: the reward of taking the action at the current state
        @param next_state: the next state after taking the action at the
            current state
        @param done: true if episode has terminated, false otherwise
        @return loss: total loss the at this time step
        """
        self.model.train()
        self.optimizer.zero_grad()
        qvals = self.model(torch.from_numpy(state).type(torch.FloatTensor))
        next_qvals = self.model(torch.from_numpy(next_state).type(torch.FloatTensor))
        if done is False:
            Target= torch.max(next_qvals)*self.gamma+reward
        else:
            Target= torch.tensor(reward)
        loss=self.lossfun(qvals[action], Target)
        #loss.requires_grad=True
        loss.backward()
        self.optimizer.step()
        return loss.detach().numpy()
        '''
        if done == True:
            reward=-1
        else:
            pass
        if done is not True:
            Target=torch.tensor(np.max(self.qvals(next_state))*self.gamma+reward)
        else: 
            Target=torch.tensor(reward)
        Q=torch.tensor(self.qvals(state)[action])
        loss=self.lossfun(Target,Q)
        #loss.requires_grad=True
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        return loss.detach().numpy()
        '''
    def save(self, outpath):
        """
        saves the model at the specified outpath
        """        
        torch.save(self.model.state_dict(), outpath)


if __name__ == '__main__':
    args = utils.hyperparameters()

    env = gym.make('CartPole-v1')
    statesize = env.observation_space.shape[0]
    actionsize = env.action_space.n

    policy = DQNPolicy(make_dqn(statesize, actionsize), statesize, actionsize, lr=args.lr, gamma=args.gamma)

    utils.qlearn(env, policy, args)

    torch.save(policy.model, 'models/dqn.model')
