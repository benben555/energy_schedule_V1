from charm.toolbox.eccurve import prime192v2
from charm.toolbox.ecgroup import ECGroup, ZR, G

# dispatch_index = 1
group = ECGroup(prime192v2)
P = group.random(G)
print(P)
q = group.order()
KW_space = ["urgent", "normal", "anyway"]
EC = {"urgent": 10, "normal": 20, "anyway": 30, "other": 40, 'a': 21, 'b': 22, 'c': 33, 'abc': 45, 'age': 29}
s = group.random(ZR)
print(s)
sk_s = s
pk_s = P ** s
print(pk_s)
sk_B1, sk_B2 = group.random(ZR), group.random(ZR)
print(sk_B1, sk_B2)
pk_B1, pk_B2 = P ** sk_B1, P ** sk_B2
