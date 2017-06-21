cities = []
with open("cities.txt", "r", encoding="utf-8") as cf:
    r = cf.read()
    l = r.split("\n")

    for city in l:
        city = city.strip()
        if city:
            if city not in cities:
                cities.append(city)
            else:
                print("Duplicate city found %" % city)


with open("cities_array.py", "w", encoding="utf-8") as cw:
    cw.write("cities = " + repr(cities))
    cw.write("\n\n")
    cw.write("cities_choices = " + repr([(city, city) for city in cities]))
