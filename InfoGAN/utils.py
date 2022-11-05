import torch
import torch.nn as nn
import numpy as np

def weights_init(m):
    if isinstance(m,nn.Conv2d):
        nn.init.normal_(m.weight.data,0.0,0.02)
    elif isinstance(m,nn.BatchNorm2d):
        nn.init.normal_(m.weight.data,1.0,0.02)
        nn.init.constant_(m.bias.data,0)

class NormalNLLLoss:
    def __call__(self,x,mu,var):
        logli=-0.5*(var.mul(2*np.pi)+1e-6).log()-(x-mu).pow(2).div(var.mul(2.0)+1e-6)
        nll=-(logli.sum(1).mean())

        return nll

def noise_sample(n_dis_c,dis_c_dim,n_con_c,n_z,batch_size,device):
    z=torch.randn(batch_size,n_z,1,1,device=device)

    idx=np.zeros((n_dis_c,batch_size))
    if n_dis_c !=0:
        dis_c=torch.zeros(batch_size,n_dis_c,dis_c_dim,device=device)

        for i in range(n_dis_c):
            idx[i]=np.random.randint(dis_c_dim,size=batch_size)
            dis_c[torch.arange(0,batch_size),i,idx[i]]=1.0
        
        dis_c=dis_c.view(batch_size,-1,1,1)

    if n_con_c!=0:
        con_c=torch.rand(batch_size,n_con_c,1,1,device=device)*2-1

    noise=z

    if n_dis_c!=0:
        noise=torch.cat((z,dis_c),dim=1)
    if n_con_c!=0:
        noise=torch.cat((noise,con_c),dim=1)
    return noise,idx