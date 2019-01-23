with open('corpus/beers.txt', mode="w") as fp:
    for i in range(99, 0, -1):
        fp.write("{n} bottles of beer on the wall, {n} bottles of beer.\n".format(n=i))
        if i == 1:
            fp.write("Take one down and pass it around, no more bottles of beer on the wall.\n")
            break
        fp.write("Take one down and pass it around, {m} bottles of beer on the wall.\n".format(m=i-1))
    fp.write("No more bottles of beer on the wall, no more bottles of beer.\n")
    fp.write("Go to the store and buy some more, 99 bottles of beer on the wall.\n")



with open('corpus/mini-beers.txt', mode="w") as fp:
    for i in range(99, 0, -1):
        fp.write("{n} bottles of beer on the wall, {n} bottles of beer.\n".format(n=i))



with open('corpus/mini-names.txt', mode="wb") as fp:
    fp.write(open('corpus/names.txt', mode="rb").read()[:5130])
