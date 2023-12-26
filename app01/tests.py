# import random
# import time
#
# from charm.toolbox.eccurve import prime192v2
# from charm.toolbox.ecgroup import ECGroup, ZR, G
# import tools
# # from backup import paillier
#
#
# def SystemSetup():
#     group = ECGroup(prime192v2)
#     P = group.random(G)
#     q = group.order()
#     KW_space = ["urgent", "normal", "anyway"]
#     EC = {"urgent": 10, "normal": 20, "anyway": 30, "other": 40, 'a': 21, 'b': 22, 'c': 33, 'abc': 45, 'age': 29}
#     GSP = {'G': group, 'P': P, 'q': q, 'KW_space': KW_space, 'EC': EC}
#     return GSP
#
#
# def ServerKeyGen(GSP):
#     s = GSP['G'].random(ZR)
#     sk_s = s
#     pk_s = GSP['P'] ** s
#     kw = random.choice(list(GSP['EC']))
#     # EC_U = GSP['EC'][kw]
#     # c1=pai.encipher(str(RC_U))
#     return (sk_s, pk_s)
#
#
# # def UserKeyGen(GSP):
# #     a1, a2 = GSP['G'].random(ZR), GSP['G'].random(ZR)
# #     sk_A = (a1, a2)
# #     pk_A1, pk_A2 = GSP['P'] ** a1, GSP['P'] ** a2
# #     pk_A = (pk_A1, pk_A2)
# #     return (sk_A, pk_A)
# def UserKeyGen(GSP):
#     a1, a2 = GSP['G'].random(ZR), GSP['G'].random(ZR)
#     sk_A = (a1, a2)
#     pk_A1, pk_A2 = GSP['P'] ** a1, GSP['P'] ** a2
#     pk_A = (pk_A1, pk_A2)
#     pai = tools.Paillier()
#     pai.__key_gen__()
#     g_U, N_U = pai.pubKey[1], pai.pubKey[0]
#     lam_U = pai.priKey[0]
#     W_U = GSP['G'].random(ZR)
#     RC_U = random.randint(1,50)
#     P_U = pai.encipher(str(RC_U))
#     return sk_A, pk_A, g_U, N_U, lam_U, RC_U, P_U, pai
#
#
# def IndexCiphertextGen(GSP, kw, pk_s, sk_A, pk_A, pk_B):
#     pk_A1, pk_A2 = pk_A
#     sk_A1, sk_A2 = sk_A
#     pk_B1, pk_B2 = pk_B
#     lambda1 = GSP['G'].hash((pk_A1, pk_B1, pk_B1 ** sk_A1))
#     lambda2 = GSP['G'].hash((pk_A2, pk_B2, pk_B2 ** sk_A2))
#     r = GSP['G'].random(ZR)
#     Q = GSP['P'] ** r * (pk_B1 ** GSP['G'].hash((kw, lambda1, lambda2))) ** r
#     IC1 = pk_s ** r
#     IC2 = GSP['G'].hash(Q)
#     IC_kw = (IC1, IC2)
#     return IC_kw
#
#
# def SearchTrapdoorGen(GSP, kw, pk_A, sk_B, pk_B):
#     pk_A1, pk_A2 = pk_A
#     sk_B1, sk_B2 = sk_B
#     pk_B1, pk_B2 = pk_B
#     lambda1 = GSP['G'].hash((pk_A1, pk_B1, pk_A1 ** sk_B1))
#     lambda2 = GSP['G'].hash((pk_A2, pk_B2, pk_A2 ** sk_B2))
#     ST_kw = GSP['G'].hash((kw, lambda1, lambda2), ZR) * sk_B1
#     return ST_kw
#
#
# def MatchTest(GSP, sk_s, IC_kw, ST_kw):
#     IC1, IC2 = IC_kw
#     Q = IC1 ** (sk_s ** -1) * (IC1 ** ST_kw) ** (sk_s ** -1)
#     return IC2 == GSP['G'].hash(Q)
#
#
# # for i in range(500):
# #     start = time.perf_counter()
# #     GSP = SystemSetup()
# #     sk_s, pk_s = ServerKeyGen(GSP)
# #     sk_A, pk_A = UserKeyGen(GSP)
# #     sk_B, pk_B = UserKeyGen(GSP)
# #     IC_kw = IndexCiphertextGen(GSP, "urgent", pk_s, sk_A, pk_A, pk_B)
# #     ST_kw = SearchTrapdoorGen(GSP, "urgent", pk_A, sk_B, pk_B)
# #     print(MatchTest(GSP, sk_s, IC_kw, ST_kw))
# #     end = time.perf_counter()
# #     print('Running time: %s Seconds' % (end - start))
# #     with open('lightweight_peaks.txt', 'a', encoding='UTF - 8') as f:
# #         data = f.write(str(end - start) + "\n")
# from django.test import TestCase
#
# # Create your tests here.
import random
import time

from charm.toolbox.eccurve import prime192v2
from charm.toolbox.ecgroup import ECGroup, ZR, G

dispatch_index = 1
group = ECGroup(prime192v2)
P = group.random(G)
print("P:", P)
temp = group.serialize(P).decode('utf-8')
print(temp)
# P: [3084503920582002655018482347830786511547281035561810084081, 68920701105273204449122128934898177880568019988840059339]
# 1:A33LuTohbgK/FgO5/EYOFl1rkJU6DP1A8Q==
b1 = "1:A33LuTohbgK/FgO5/EYOFl1rkJU6DP1A8Q==".encode('utf-8')
b1 = group.deserialize(b1)
print(b1)
print(type(b1))
# print("b1:",b1)
# print(P==b1)
s = group.random(ZR)
print("s:", s)
temp = group.serialize(s).decode('utf-8')
print(temp)
sk_s = s
pk_s = P ** s
print("pk_s:", pk_s)
temp = group.serialize(pk_s).decode('utf-8')
print(temp)
sk_B1, sk_B2 = group.random(ZR), group.random(ZR)
print("sk_B1", sk_B1)
temp = group.serialize(sk_B1).decode('utf-8')
print(temp)
print("sk_B2:", sk_B2)
temp = group.serialize(sk_B2).decode('utf-8')
print(temp)
pk_B1, pk_B2 = P ** sk_B1, P ** sk_B2
print("pk_B1:", pk_B1)
temp = group.serialize(pk_B1).decode('utf-8')
print(temp)
print("pk_B2:", pk_B2)
temp = group.serialize(pk_B2).decode('utf-8')
print(temp)
# P: [4509187802710272973390721486574992821020243518316702949598, 1619857729791368720982076666908306546194391603043431195771]
# 1:A7fmHge/Q0FdFJLnj+rXnXmYYoJaBlFg3g==
# [3084503920582002655018482347830786511547281035561810084081, 68920701105273204449122128934898177880568019988840059339]
# <class 'elliptic_curve.Element'>
# s: 4586255674612501977513897526121916553732356753106935020753
# 0:uwq+UY1vQy7KPiwxQVl2Wv2dgSdI8PzR
# pk_s: [4910718883154288638296174285393037863882632472365242575533, 6236954442306809453862233437747288014276356664398186389614]
# 1:AshGTCHP34jzYDG+KFm/tigGw7sxxXDqrQ==
# sk_B1 6027293236460033846010295777633959028798460247977453638742
# 0:9c/gqOfZqaj/oBheqJmiLa86Zar+71RW
# sk_B2: 1055885301823768296459596664356445448511610397006654039577
# 0:Kw/0+P2ZXAZWUDTBrHA0eoLGigonL2YZ
# pk_B1: [3566220860877372820409935905772261328060817242460822571800, 3173812091440156514167824525272718238366470378099572713012]
# 1:ApFxFUPt0t5UeyZXbYyYcriqdsBzqiILGA==
# pk_B2: [4714276314855727145359878552254644950966810577314308409496, 3994004862357464900455803796179177495779066194410594353505]
# 1:A8BDV14zRgYuU8oIPeCiTZDWNO+Ez2/ImA==
