import torch


class QTable:
    def __init__(self, path):
        self.table = torch.load(path, weights_only=True) if path else torch.zeros(3 ** 9, 9).to("cuda")
        self.gamma = 0.8

    def update(self, last_num_state, last_action, current_num_state, valid_places):
        if last_num_state is None or last_action is None:
            return
        rewards = {"won": 100, "draw": -1, "lose": -100}
        if current_num_state in rewards:
            self.table[last_num_state, last_action] = rewards[current_num_state]
        else:
            max_value = max(self.table[current_num_state].tolist()[index] for index in valid_places)
            self.table[last_num_state, last_action] = self.gamma * max_value

    def showQValues(self, num_state):
        print("Q values:")
        temp = self.table[num_state].tolist()
        print(temp[:3])
        print(temp[3:6])
        print(temp[6:])
        print("---------------")
