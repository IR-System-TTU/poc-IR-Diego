dic = {}
dic[('Testicide', -9)] = 1
dic[('Pesticide', 4)] = 1
new_out = dict(sorted(dic.items(), key = lambda element: element[0][1] * element[0][0]))
print(new_out)
print(new_out.keys().__contains__(('Pesticide')))
