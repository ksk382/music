from joint_get_bands import KEXP_charts


a = KEXP_charts(50)

x = 1
for i in a:
    print ('{0} - {1} {2}'.format(x, i.name, i.appeared))
    x +=1