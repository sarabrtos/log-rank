import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from lifelines.statistics import logrank_test


import seaborn as sns

# ==========================================
# Ler planilha
# ==========================================

df = pd.read_excel("/home/sara/Documentos/latiik.xlsx")

# ordem dos grupos

ordem = [
    "SAL",
    "DZP",
    "API 50",
    "API 150",
    "API 450",
    "M API 50",
    "M API 150",
    "M API 450"
]

df["grupo"] = pd.Categorical(df["grupo"],
                             categories=ordem,
                             ordered=True)

# ==========================================
# cores
# ==========================================

cores = {
    "SAL":"#716f6f",
    "DZP":"#a8cd14",
    "API 50":"#760687",
    "API 150":"#760687",
    "API 450":"#760687",
    "M API 50":"#9f75a5",
    "M API 150":"#9f75a5",
    "M API 450":"#9f75a5"
}

# ==========================================
# log-rank
# ==========================================

controle = df[df.grupo=="SAL"]

p = []
comparacoes = []

for g in ordem[1:]:

    teste = logrank_test(
        controle["tempo"],
        df[df.grupo==g]["tempo"],
        event_observed_A=controle["evento"],
        event_observed_B=df[df.grupo==g]["evento"]
    )

    comparacoes.append(("SAL",g))
    p.append(teste.p_value)

# ==========================================
# função dos asteriscos
# ==========================================

def estrelas(p):

    if p < 0.0001:
        return "****"
    elif p < 0.001:
        return "***"
    elif p < 0.01:
        return "**"
    elif p < 0.05:
        return "*"
    else:
        return "ns"

# ==========================================
# Figura
# ==========================================

plt.figure(figsize=(8,6),dpi=120)

# violino

sns.violinplot(
    data=df,
    x="grupo",
    y="tempo",
    palette=cores,
    inner=None,
    cut=0,
    linewidth=1
)

# pontos

sns.stripplot(
    data=df[df.evento==1],
    x="grupo",
    y="tempo",
    palette=cores,
    jitter=0.15,
    size=5,
    edgecolor="black",
    linewidth=0.4
)

# censurados

for i,g in enumerate(ordem):

    cens=df[(df.grupo==g)&(df.evento==0)]

    x=np.random.normal(i,0.05,len(cens))

    plt.scatter(
        x,
        cens["tempo"],
        marker="^",
        s=55,
        color=cores[g],
        edgecolor="black",
        linewidth=0.4,
        zorder=10
    )

# ==========================================
# colchetes
# ==========================================

def bracket(x1,x2,y,text):

    plt.plot(
        [x1,x1,x2,x2],
        [y,y+8,y+8,y],
        color="black",
        lw=1.2
    )

    plt.text(
        (x1+x2)/2,
        y+11,
        text,
        ha="center",
        fontsize=12
    )

altura = 640

for i, pv in enumerate(p):

    if pv < 0.05:

        bracket(
            0,
            i+1,
            altura,
            estrelas(pv)
        )

        altura += 25

# ==========================================
# legenda
# ==========================================

from matplotlib.lines import Line2D

legenda=[
    Line2D([],[],
           marker='o',
           linestyle='',
           color='black',
           label='Event'),

    Line2D([],[],
           marker='^',
           linestyle='',
           color='black',
           label='Censored')
]

plt.legend(
    handles=legenda,
    frameon=False,
    bbox_to_anchor=(1.02,1),
    loc="upper left"
)

plt.ylabel("Latency (s)",fontsize=14)
plt.xlabel("")
plt.ylim(0,700)

plt.xticks(rotation=45)

sns.despine()

plt.tight_layout()

plt.show()