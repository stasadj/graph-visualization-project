# SOK Projekat 2020/2021 -Tim 15 :computer:

## Članovi tima
* SW-37-2018 Nenad Petković
* SW-45-2018 Jelena Miletić
* SW-48-2018 Anastasija Đurić
* SW-52-2018 Dina Petrov

## Komponente
* CORE - jezgro programa i ujedno i Django aplikacija
* XMLDataLoader - učitavanje XML fajlova
* DeezerDataLoader - učitavanje podataka o *Deezer* plejlistama
* SimpleVizualization - jednostavan prikaz podataka u vidu grafa
* ComplexVizualization - složeni prikaz podataka u vidu grafa


## Uputstvo za instalaciju komponenti


1. Pozicionirati se na željenu putanju u git bash-u i kucati:
```
git clone https://gitlab.com/sok_2020_2021/tim15.git
```
  

2. Poželjno je koristiti virtuelno okruženje:

    2.1 Instalirati pip po uputstvu : https://pip.pypa.io/en/stable/installing/
    
    2.2. Instalirati virtuealenv alat:

    ```
    pip install virtualenv
    ```
    
    2.3. Kreirati novo virtuelno okruženje komandom:
    
    ```
    virtualenv NAZIV_OKRUZENJA
    ```
    
    2.4. Aktivirati okruženje komandama:
    
    * Za Windows
        
        ```
        NAZIV_OKRUZENJA\Scripts\activate
        ```
        
    * Za UNIX
        
        ```
        source NAZIV_OKRUZENJA/bin/activate
        ```
        
3. Za svaku od gore-navedenih komponenti, potrebno je pozicionirati se u njihov direktorijum i instalirati ih komandom:

```
python setup.py install
```

4. Kako bi *DeezerDataLoader* komponenta pravilno radila, potrebno je instalirati i **requests** HTTP biblioteku:

```
pip install requests
```

## Parametrizacija Django projekta

5. Instalirati Django u virtuelnom okruženju komandom:

```
pip install Django
```

6. Pozicionirati se u **django_project** direktorijum i pokrenuti server komandom

```
python manage.py runserver
```

## Uputstvo za upotrebu
U gornjem levom uglu se bira iz drop-down menija željena komponenta za učitavanje podataka.   
Potom se unosi link ka Deezer plejlisti ili bira .xml fajl iz fajl sistema, u zavisnosti od   
odabrane komponente.  
Nakon uspešnog učitavanja podataka, sledi odabir vizualizacione komponente.  
Sa desne strane ekrana je dinamički prikaz podataka u obliku stabla (eng. *tree view*).   
Ispod stabla nalazi se umanjeni prikaz grafa u ptičjoj perspektivi (eng. *bird view*).   
Duplim klikom na element stabla dobijaju se dodatne informacije o selektovanom entitetu.   
Stablo podržava i ciklične grafove, te je moguće beskonačno iči u dubinu.  
Desno od stabla nalazi se glavni prikaz grafa (eng. *main view*)  
koji podržava zumiranje, pomeranje celog grafa i pomeranje pojedinačnih čvorova.  
Graf je moguće pretraživati i filtrirati po nazivu i atributima unosom teksta u polje iznad grafa  
Pri filtriranju neophodno je uneti tekst u obliku:
```
<naziv_atributa> <poredbeni_operator> <željena_vrednost>
```
Podržani poredbeni operatori su:
```
==, !=, <, <=, >, >=
```
 
