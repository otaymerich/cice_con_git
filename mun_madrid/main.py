import requests as req
import json
import matplotlib.pyplot as plt

url = "https://datos.comunidad.madrid/catalogo/dataset/032474a0-bf11-4465-bb92-392052962866/resource/301aed82-339b-4005-ab20-06db41ee7017/download/municipio_comunidad_madrid.json"
res = req. get(url).json()
data = res["data"]

# obtener municipio por codigo INE
def get_by_ine(ine):
    for mun in data:
        if mun["municipio_codigo_ine"] == ine:
            return mun

# obtener el municipio más grande
def mun_mayor():
    mun_mas_grande = None
    area = 0
    for mun in data:
        if mun["superficie_km2"] > area:
            mun_mas_grande = mun
            area = mun["superficie_km2"]
    return mun_mas_grande

# obtener superficie total
def sup_total():
    superficie = sum([mun["superficie_km2"] for mun in data])
    return superficie



# densidad de poblacion total
def dens_total(): #en realidad es densidad media (suma de densidades no tiene ningun sentido numerico)
    superficie = 0
    habitantes = 0
    for mun in data:
        superficie += mun["superficie_km2"]
        habitantes += mun["superficie_km2"] * mun["densidad_por_km2"]
    return habitantes/superficie

# obtener la población de Madrid
def pob_madrid():
    superf_total = sup_total()
    data.remove(mun_mayor())
    sup_sin_madrid = sup_total()
    return superf_total - sup_sin_madrid

# obtener poblacion media municipios
def pob_media():
    densidad = dens_total()
    superficie_total = sup_total()
    sup_media = superficie_total/len(data)
    return densidad * sup_media


#comprovar ley de Benford
def benford(numero): # primera opcion que hice
    num_list = []
    total_num = 0
    for mun in data:
        num_list.append(mun["densidad_por_km2"])
        # num_list.append(mun["superficie_km2"]) 
    for i in num_list:
        if str(i)[0] == str(numero):
            total_num += 1
    return total_num/len(num_list)

def benford_grpah():
    benford_list = []
    num_list = []
    for i in range(1,10):
        num_list.append(i)
        benford_list.append(round(benford(i)*100,2))
        print(f"{i}: {round(benford(i)*100,2)}%")
    plt.plot(num_list, benford_list)
    plt.show()

def benford_2():
    provab = {str(k): 0 for k in range(1,10)}
    for mun in data:
        first_dig = str(mun["densidad_por_km2"])[0]
        provab[first_dig] += 100/len(data)
    for i in provab.keys():
        provab[i] = round(provab[i],2)
    return provab

def benford_3():
    provab = {}
    for mun in data:
        first_dig = str(mun["densidad_por_km2"])[0]
        try:
            provab[first_dig] += 100/len(data)
        except KeyError:
            provab[first_dig] = 100/len(data)
    return provab
            
        

plt.style.use('_mpl-gallery')
fig, ax = plt.subplots()
ax.bar(range(1,10), benford_3().values(), width=1, edgecolor="white", linewidth=0.7)
plt.show()
# plt.savefig("charge.png")