import torch
import torch.nn as nn
import torch.nn.functional as F


class Actor(torch.nn.Module):
    def __init__(self, action_space):
        super(Actor, self).__init__()
        self.input_channel = 1
        self.action_space = action_space
        channel_cnn = 128 
        channel_fc = 128
        self.actor_conv1 = nn.Conv1d(self.input_channel, channel_cnn, 4)
        self.actor_conv2 = nn.Conv1d(self.input_channel, channel_cnn, 4)
        self.actor_conv3 = nn.Conv1d(self.input_channel, channel_cnn, 4)
        self.actor_fc_1 = nn.Linear(self.input_channel, channel_fc)
        self.actor_fc_2 = nn.Linear(self.input_channel, channel_fc)
        self.actor_fc_3 = nn.Linear(self.input_channel, channel_fc)

        incoming_size = 2*channel_cnn*5 + 1 * channel_cnn*3 + 3 * channel_fc

        self.fc1 = nn.Linear(in_features=incoming_size, out_features= channel_fc)
        self.fc2 = nn.Linear(in_features=channel_fc, out_features=self.action_space)

    def forward(self, inputs):
        throughputs_batch = inputs[:, 2:3, :]
        download_time_batch = inputs[:, 3:4, :]
        sizes_batch = inputs[:, 4:5, :self.action_space]

        x_1 = F.relu(self.actor_conv1(throughputs_batch))
        x_2 = F.relu(self.actor_conv2(download_time_batch))
        x_3 = F.relu(self.actor_conv3(sizes_batch))
        x_4 = F.relu(self.actor_fc_1(inputs[:, 0:1, -1]))
        x_5 = F.relu(self.actor_fc_2(inputs[:, 1:2, -1]))
        x_6 = F.relu(self.actor_fc_3(inputs[:, 5:6, -1]))

        x_1 = x_1.view(-1, self.num_flat_features(x_1))
        x_2 = x_2.view(-1, self.num_flat_features(x_2))
        x_3 = x_3.view(-1, self.num_flat_features(x_3))
        x_4 = x_4.view(-1, self.num_flat_features(x_4))
        x_5 = x_5.view(-1, self.num_flat_features(x_5))
        x_6 = x_6.view(-1, self.num_flat_features(x_6))

        x = torch.cat([x_1, x_2, x_3, x_4, x_5, x_6], 1)
        x = F.relu(self.fc1(x))
        actor = F.softmax(self.fc2(x), dim=1)
        return actor

    def num_flat_features(self,x):
        size=x.size()[1:]
        num_features=1
        for s in size:
            num_features*=s
        return num_features

class Critic(torch.nn.Module):
    def __init__(self, action_space):
        super(Critic, self).__init__()
        self.input_channel = 1
        self.action_space = action_space
        channel_cnn = 128 
        channel_fc = 128
        self.critic_conv1 = nn.Conv1d(self.input_channel, channel_cnn, 4)
        self.critic_conv2 = nn.Conv1d(self.input_channel, channel_cnn, 4)
        self.critic_conv3 = nn.Conv1d(self.input_channel, channel_cnn, 4)
        self.critic_fc_1 = nn.Linear(self.input_channel, channel_fc)
        self.critic_fc_2 = nn.Linear(self.input_channel, channel_fc)
        self.critic_fc_3 = nn.Linear(self.input_channel, channel_fc)

        incoming_size = 2*channel_cnn*5 + 1 * channel_cnn*3 + 3 * channel_fc

        self.fc1 = nn.Linear(in_features=incoming_size, out_features= channel_fc)
        self.fc2 = nn.Linear(in_features=channel_fc, out_features=1)

    def forward(self, inputs):
        throughputs_batch = inputs[:, 2:3, :] 
        download_time_batch = inputs[:, 3:4, :]
        sizes_batch = inputs[:, 4:5, :self.action_space]

        x_1 = F.relu(self.critic_conv1(throughputs_batch))
        x_2 = F.relu(self.critic_conv2(download_time_batch))
        x_3 = F.relu(self.critic_conv3(sizes_batch))
        x_4 = F.relu(self.critic_fc_1(inputs[:, 0:1, -1]))
        x_5 = F.relu(self.critic_fc_2(inputs[:, 1:2, -1]))
        x_6 = F.relu(self.critic_fc_3(inputs[:, 5:6, -1]))

        x_1 = x_1.view(-1, self.num_flat_features(x_1))
        x_2 = x_2.view(-1, self.num_flat_features(x_2))
        x_3 = x_3.view(-1, self.num_flat_features(x_3))
        x_4 = x_4.view(-1, self.num_flat_features(x_4))
        x_5 = x_5.view(-1, self.num_flat_features(x_5))
        x_6 = x_6.view(-1, self.num_flat_features(x_6))

        x = torch.cat([x_1, x_2, x_3, x_4, x_5, x_6], 1)
        x = F.relu(self.fc1(x))
        critic = self.fc2(x)
        return critic

    def num_flat_features(self,x):
        size=x.size()[1:]
        num_features=1
        for s in size:
            num_features*=s
        return num_features
    
# class Actor(torch.nn.Module):
#     def __init__(self, action_space):
#         super(Actor, self).__init__()
#         self.input_channel = 1
#         self.action_space = action_space
#         self.future_steps = 5
#         channel_cnn = 128 
#         channel_fc = 128
#         self.actor_conv1 = nn.Conv1d(self.input_channel, channel_cnn, 4)
#         self.actor_conv2 = nn.Conv1d(self.input_channel, channel_cnn, 4)
#         self.actor_conv3 = nn.Conv1d(self.input_channel, channel_cnn, 4)
#         self.actor_fc_1 = nn.Linear(self.input_channel, channel_fc)
#         self.actor_fc_2 = nn.Linear(self.input_channel, channel_fc)
#         self.actor_fc_3 = nn.Linear(self.input_channel, channel_fc)
#         self.actor_fc_future = nn.Linear(self.input_channel, channel_fc)
#         incoming_size = 2*channel_cnn*5 + 1 * channel_cnn*3 + 4 * channel_fc #
#         self.fc1 = nn.Linear(in_features=incoming_size, out_features= channel_fc)
#         self.fc2 = nn.Linear(in_features=channel_fc, out_features=self.action_space)

#     def forward(self, inputs):
#         throughputs_batch = inputs[:, 2:3, :]
#         download_time_batch = inputs[:, 3:4, :]
#         sizes_batch = inputs[:, 4:5, :self.action_space]
#         x_1 = F.relu(self.actor_conv1(throughputs_batch))
#         x_2 = F.relu(self.actor_conv2(download_time_batch))
#         x_3 = F.relu(self.actor_conv3(sizes_batch))
#         x_4 = F.relu(self.actor_fc_1(inputs[:, 0:1, -1]))
#         x_5 = F.relu(self.actor_fc_2(inputs[:, 1:2, -1]))
#         x_6 = F.relu(self.actor_fc_3(inputs[:, 5:6, -1]))
#         x_future = F.relu(self.actor_fc_future(inputs[:, 6:7, -1]))
#         x_1 = x_1.view(-1, self.num_flat_features(x_1))
#         x_2 = x_2.view(-1, self.num_flat_features(x_2))
#         x_3 = x_3.view(-1, self.num_flat_features(x_3))
#         x_4 = x_4.view(-1, self.num_flat_features(x_4))
#         x_5 = x_5.view(-1, self.num_flat_features(x_5))
#         x_6 = x_6.view(-1, self.num_flat_features(x_6))
#         x_future = x_future.view(-1, self.num_flat_features(x_future))
#         x = torch.cat([x_1, x_2, x_3, x_4, x_5, x_6, x_future], 1)
#         x = F.relu(self.fc1(x))
#         actor = F.softmax(self.fc2(x), dim=1)
#         return actor

#     def num_flat_features(self,x):
#         size=x.size()[1:]
#         num_features=1
#         for s in size:
#             num_features*=s
#         return num_features

# class Critic(torch.nn.Module):
#     def __init__(self, action_space):
#         super(Critic, self).__init__()
#         self.input_channel = 1
#         self.action_space = action_space
#         channel_cnn = 128 
#         channel_fc = 128
#         self.critic_conv1 = nn.Conv1d(self.input_channel, channel_cnn, 4)
#         self.critic_conv2 = nn.Conv1d(self.input_channel, channel_cnn, 4)
#         self.critic_conv3 = nn.Conv1d(self.input_channel, channel_cnn, 4)
#         self.critic_fc_1 = nn.Linear(self.input_channel, channel_fc)
#         self.critic_fc_2 = nn.Linear(self.input_channel, channel_fc)
#         self.critic_fc_3 = nn.Linear(self.input_channel, channel_fc)
#         self.critic_fc_future = nn.Linear(self.input_channel, channel_fc)
#         incoming_size = 2*channel_cnn*5 + 1 * channel_cnn*3 + 4 * channel_fc
#         self.fc1 = nn.Linear(in_features=incoming_size, out_features= channel_fc)
#         self.fc2 = nn.Linear(in_features=channel_fc, out_features=1)

#     def forward(self, inputs):
#         throughputs_batch = inputs[:, 2:3, :] 
#         download_time_batch = inputs[:, 3:4, :]
#         sizes_batch = inputs[:, 4:5, :self.action_space]
#         x_1 = F.relu(self.critic_conv1(throughputs_batch))
#         x_2 = F.relu(self.critic_conv2(download_time_batch))
#         x_3 = F.relu(self.critic_conv3(sizes_batch))
#         x_4 = F.relu(self.critic_fc_1(inputs[:, 0:1, -1]))
#         x_5 = F.relu(self.critic_fc_2(inputs[:, 1:2, -1]))
#         x_6 = F.relu(self.critic_fc_3(inputs[:, 5:6, -1]))
#         x_future = F.relu(self.critic_fc_future(inputs[:, 6:7, -1]))
#         x_1 = x_1.view(-1, self.num_flat_features(x_1))
#         x_2 = x_2.view(-1, self.num_flat_features(x_2))
#         x_3 = x_3.view(-1, self.num_flat_features(x_3))
#         x_4 = x_4.view(-1, self.num_flat_features(x_4))
#         x_5 = x_5.view(-1, self.num_flat_features(x_5))
#         x_6 = x_6.view(-1, self.num_flat_features(x_6))
#         x_future = x_future.view(-1, self.num_flat_features(x_future))
#         x = torch.cat([x_1, x_2, x_3, x_4, x_5, x_6, x_future], 1)
#         x = F.relu(self.fc1(x))
#         critic = self.fc2(x)
#         return critic

#     def num_flat_features(self,x):
#         size=x.size()[1:]
#         num_features=1
#         for s in size:
#             num_features*=s
#         return num_features