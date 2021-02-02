# SOK Projekat 2020/2021 -Tim 15 :computer:

## Članovi tima
* SW-37-2018 Nenad Petković
* SW-45-2018 Jelena Miletić
* SW-48-2018 Anastasija Đurić
* SW-52-2018 Dina Petrov

## Komponente
* CORE - jezgro aplikacije
* XMLDataLoader - učitavanje XML fajlova
* DeezerDataLoader - učitavanje podataka o *Deezer* plejlistama
* SimpleVizualization - jednostavan prikaz podataka u vidu grafa
* ComplexVizualization - složeni prikaz podataka u vidu grafa


## Uputstvo za instalaciju komponenti
Potrebno je pozicionirati se u direktorijum svake komponente i pokrenuti komandu:

```
python setup.py install
```


Kako bi *DeezerDataLoader* komponenta pravilno radila, potrebno je instalirati i **requests** HTTP biblioteku:


```
pip install requires
```

## Parametrizacija Django projekta