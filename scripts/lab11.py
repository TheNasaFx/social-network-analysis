import networkx as nx
from linkpred.predictors import Jaccard, AdamicAdar
from sklearn.tree import DecisionTreeClassifier
import numpy as np

# Граф үүсгэх (жишээ болгон таны өгөгдлөөс санаа авсан)
g = nx.Graph()
g.add_edges_from([
    ('RED_PRIEST', 'KINVARA'), ('LITTLE_SAM', 'DICKON'), 
    ('TOMMEN', 'MACE'), ('JOFFREY', 'CAMELLO'), 
    ('OLD_NAN', 'BENJEN'), ('NED', 'LADY_CRANE'), 
    ('NED', 'CLARENZO'), ('SANSA', 'ROBB'), 
    ('LADY_CRANE', 'CLARENZO')  # Таны гаралтаас нэмсэн
])

# 1. Jaccard тооцоолол
print("Jaccard-ийн топ 5 хос:")
jc = Jaccard(g, excluded=g.edges())
jc_results = jc.predict()
top_jc = jc_results.top(5)
for edge, score in top_jc.items():
    print(f"{edge[0]} - {edge[1]} {score}")

# 2. Adamic Adar тооцоолол
print("\nAdamic Adar-ийн топ 5 хос:")
aa = AdamicAdar(g, excluded=g.edges())
aa_results = aa.predict()
top_aa = aa_results.top(5)
for edge, score in top_aa.items():
    print(f"{edge[0]} - {edge[1]} {score}")

# 3. Decision Tree сургалт
X = []  # Онцлог (Jaccard, Adamic Adar оноо)
y = []  # Шошго (1 = холбоос байгаа, 0 = байхгүй)

# Одоо байгаа холбоосууд
for edge in g.edges():
    try:
        X.append([jc_results[edge], aa_results[edge]])
        y.append(1)
    except KeyError:
        continue

# Байхгүй холбоосууд (Jaccard-ийн топ 5-аас)
for edge, score in jc_results.top(5).items():
    if edge not in g.edges():
        try:
            X.append([score, aa_results[edge]])
            y.append(0)
        except KeyError:
            continue

# X, y-г 2D массив болгох
X = np.array(X)
y = np.array(y)

# Хэрэв X хоосон биш бол
if X.size > 0:
    clf = DecisionTreeClassifier()
    clf.fit(X, y)
    
    # Шинэ хосын таамаглал
    new_pair = np.array([[0.7, 2.5]])  # Жишээ онцлог
    prediction = clf.predict(new_pair)
    print("\nШинэ хосын таамаглал (0.7, 2.5):")
    print(f"Холбоос байгаа эсэх: {prediction[0]}")
else:
    print("\nАлдаа: Онцлог хоосон байна.")