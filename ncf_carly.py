import torch
from torch import nn
from torch.nn.init import xavier_uniform_, xavier_normal_
from torch.nn.parameter import Parameter

class NCF(nn.Module):
    """The neural collaborative filtering method.
    """
    def __init__(self, config, data, debiasing=False, output_dim=2):
        super(NCF, self).__init__()
        self.task = config['task']

        self.debiasing = debiasing
        #self.embedding_size = int(config['embedding_size'])
        self.loss_type = config['loss_type']

        self.n_users = data.n_users
        self.n_items = data.n_items
        self.embedding_size = int(config['embedding_size'])


        ##width annd height,, creating the user and item embeddings
        self.W = torch.nn.Embedding(self.n_users, self.embedding_size)
        self.H = torch.nn.Embedding(data.n_items, self.embedding_size)

        self.linear_1 = torch.nn.Linear(self.embedding_size*2, self.embedding_size)
        self.relu = torch.nn.ReLU()
        self.linear_2 = torch.nn.Linear(self.embedding_size, 1, bias=False)
        self.sigmoid = torch.nn.Sigmoid()

        self.xent_func = torch.nn.BCELoss()



    def forward(self, x, is_training=False):
        user_idx = torch.LongTensor(x[:,0])
        item_idx = torch.LongTensor(x[:,1])
        U_emb = self.W(user_idx)
        V_emb = self.H(item_idx)

        # concat
        z_emb = torch.cat([U_emb, V_emb], axis=1)

        h1 = self.linear_1(z_emb)
        h1 = self.relu(h1)

        out = self.linear_2(h1)

        # out = torch.sum(U_emb.mul(V_emb), 1)

        if is_training:
            return out, U_emb, V_emb
        else:
            return out

# fittng to training data
    def fit(self, x, y, num_epoch=1000, lr=0.05, lamb=0, tol=1e-4, batch_size=128, verbose=0):
        optimizer = torch.optim.Adam(self.parameters(), lr=lr, weight_decay=lamb)
        last_loss = 1e9

        num_sample = len(x)
        total_batch = num_sample // batch_size

        early_stop = 0
        for epoch in range(num_epoch):
            all_idx = np.arange(num_sample)
            np.random.shuffle(all_idx)
            epoch_loss = 0
            for idx in range(total_batch):
                # mini-batch training
                selected_idx = all_idx[batch_size*idx:(idx+1)*batch_size]
                sub_x = x[selected_idx]
                sub_y = y[selected_idx]

                optimizer.zero_grad()
                pred, u_emb, v_emb = self.forward(sub_x, True)

                pred = self.sigmoid(pred)

                xent_loss = self.xent_func(pred, torch.unsqueeze(torch.Tensor(sub_y),1))

                loss = xent_loss
                loss.backward()
                optimizer.step()
                epoch_loss += xent_loss.detach().numpy()

            relative_loss_div = (last_loss-epoch_loss)/(last_loss+1e-10)
            if  relative_loss_div < tol:
                if early_stop > 5:
                    print("[NCF] epoch:{}, xent:{}".format(epoch, epoch_loss))
                    break
                early_stop += 1
                
            last_loss = epoch_loss

            if epoch % 10 == 0 and verbose:
                print("[NCF] epoch:{}, xent:{}".format(epoch, epoch_loss))

            if epoch == num_epoch - 1:
                print("[Warning] Reach preset epochs, it seems does not converge.")

    def partial_fit(self, x, y, num_epoch=1000, lr=0.05, lamb=0, tol=1e-4):
        self.fit(x, y, num_epoch=1000, lr=0.05, lamb=0, tol=1e-4)

    def calculate_loss(self, interaction):
        user = interaction['user']
        item = interaction['item']
        itemage = interaction['itemage']
        pred = self.forward(user, item, itemage)
        target = interaction['target'].float()
        loss = self.loss_fct(pred, target)
        # if self.debiasing:
        #     ctr = torch.reciprocal(interaction['ctr']) # [B]
        #     loss = torch.mul(loss, ctr).sum() # [B] -> [1]
        return loss


    def predict(self, x):
        pred = self.forward(x)
        pred = self.sigmoid(pred)
        return pred.detach().numpy().flatten()

    def predict_proba(self, x):
        pred = self.forward(x)
        pred = pred.reshape(-1,1)
        pred = self.sigmoid(pred)
        return np.concatenate([1-pred,pred],axis=1)