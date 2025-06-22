tuyaux = []

with open('niveau2.txt', 'r') as file:
    for line in file:
        line = line.strip()
        if line == '' or line.startswith('#'):
            continue
        parts = line.split(',')
        if len(parts) < 9:
            continue
        x = int(parts[0])
        y = int(parts[1])
        width = int(parts[2])
        height = int(parts[3])
        flag = int(parts[8])

        # Filtrer les tuyaux : flag=1 et largeur > 50 (critère à adapter)
        if flag == 1 and width >= 50:
            tuyaux.append({'x': x, 'y': y, 'width': width, 'height': height})

print("Tuyaux trouvés dans niveau2.txt:")
for t in tuyaux:
    print(t)
