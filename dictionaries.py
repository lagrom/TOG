en_de = {"Austria":"Vienna", "Switzerland":"Bern", "Germany":"Berlin", "Netherlands":"Amsterdam"}
capitals = {"Austria":"Vienna", "Germany":"Berlin", "Netherlands":"Amsterdam"}
capital = capitals.pop("Austria")
print(capital)

d = {"a":123, "b":34, "c":304, "d":99}
for key in d:
     print(key) 
     print(d[key])

for value in d.values():
    print(value)


w = {"house": "Haus", "cat": "", "red": "rot"}
items_view = w.items()
items = list(items_view)
items

keys_view = w.keys()
keys = list(keys_view)
keys

values_view = w.values()
values = list(values_view)
values

w.items()
