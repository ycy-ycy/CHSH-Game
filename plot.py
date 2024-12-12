import numpy as np
import matplotlib.pyplot as plt
import os

pi = np.pi
pi2 = pi/2

saveBasisName = 'data/basis.png'
saveCurveName = 'data/winningNoise.png'

def plotBasis(diff_a, diff_0, diff_b, filename):
    fig, ax = plt.subplots(1,4,figsize=(7,3))
    for i in range(4):
        ax[i].axis('off')
        ax[i].grid(False)
        ax[i].set_aspect('equal')
        ax[i].set_xlim(-1.5,1.5)
        ax[i].set_ylim(-1.5,1.5)

    delta = 0.25
    r = 1.2

    ax[0].arrow(0,0,1,0,color='k', head_width=0.1, head_length=0.2)
    ax[0].text(r*np.cos(delta), r*np.sin(delta), '$|0\\rangle$', color=(0,0,0,0.8))
    ax[0].arrow(0,0,0,1,color='k', head_width=0.1, head_length=0.2)
    ax[0].text(r*np.cos(-delta+pi2), r*np.sin(-delta+pi2), '$|1\\rangle$', color=(0,0,0,0.8))
    ax[0].set_title('Alice Basis 0')

    ax[1].arrow(0,0,np.cos(diff_a),np.sin(diff_a),color='k', head_width=0.1, head_length=0.2)
    ax[1].text(r*np.cos(diff_a+delta), r*np.sin(diff_a+delta), '$|0\\rangle$', color=(0,0,0,0.8))
    ax[1].arrow(0,0,np.cos(diff_a+pi2),np.sin(diff_a+pi2),color='k', head_width=0.1, head_length=0.2)
    ax[1].text(r*np.cos(diff_a-delta+pi2), r*np.sin(diff_a-delta+pi2), '$|1\\rangle$', color=(0,0,0,0.8))
    ax[1].set_title('Alice Basis 1')

    ax[2].arrow(0,0,np.cos(diff_0),np.sin(diff_0),color='k', head_width=0.1, head_length=0.2)
    ax[2].text(r*np.cos(diff_0+delta), r*np.sin(diff_0+delta), '$|0\\rangle$', color=(0,0,0,0.8))
    ax[2].arrow(0,0,np.cos(diff_0+pi2),np.sin(diff_0+pi2),color='k', head_width=0.1, head_length=0.2)
    ax[2].text(r*np.cos(diff_0-delta+pi2), r*np.sin(diff_0-delta+pi2), '$|1\\rangle$', color=(0,0,0,0.8))
    ax[2].set_title('Bob Basis 0')

    ax[3].arrow(0,0,np.cos(diff_0+diff_b),np.sin(diff_0+diff_b),color='k', head_width=0.1, head_length=0.2)
    ax[3].text(r*np.cos(diff_0+diff_b+delta), r*np.sin(diff_0+diff_b+delta), '$|0\\rangle$', color=(0,0,0,0.8))
    ax[3].arrow(0,0,np.cos(diff_0+diff_b+pi2),np.sin(diff_0+diff_b+pi2),color='k', head_width=0.1, head_length=0.2)
    ax[3].text(r*np.cos(diff_0+diff_b-delta+pi2), r*np.sin(diff_0+diff_b-delta+pi2), '$|1\\rangle$', color=(0,0,0,0.8))
    ax[3].set_title('Bob Basis 1')

    fig.tight_layout()
    path = os.path.dirname(filename)
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

if saveBasisName:
    plotBasis(pi/4, pi/8, -pi/4, saveBasisName)
    
if saveCurveName:
    data = []
    err = []
    with open('data/imperfectPreparation.txt', 'r') as f:
        for i in range(101):
            e = float(f.readline().strip().split(':')[1].strip())
            err.append(e)
            for j in range(4):
                f.readline()
            d = float(f.readline().strip().split(':')[1].split('(')[0].strip())
            data.append(d)
            f.readline()

    plt.scatter(err, data, s=10)
    plt.xlabel('Error Rate')
    plt.ylabel('Winning Probability')
    plt.title('Winning Probability vs Error Rate')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(saveCurveName, dpi=300, bbox_inches='tight')
    plt.close()