data = [(b'481248489238429727', b'Anunaki_f0x#0001', 50), (b'481248489238429727', b'yake#6312', 53), (b'481248489238429727', b'\xf0\x9d\x95\xbd\xf0\x9d\x96\x8e\xf0\x9d\x96\x96\xf0\x9d\x96\x9f#5773', 92), (b'481248489238429727', b'Ramo#4907', 745)]
new_data = list()
for data_set in data:
    entry = list()
    for item in data_set:
        if isinstance(item, bytes):
            entry.append(item.decode())
        else:
            entry.append(item)
    new_data.append(entry)

print(new_data)