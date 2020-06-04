# Informacje

 - Implementacja algorytmu **MinCount** znajduje się w pliku `min_count.py`.
 - Implementacja algorytmu **HyperLogLog** znajduje się w pliku `hyper_log_log.py`.
 - Plik `hash_functions.py` zawiera implementacje użytych w testach funkcji haszujących.
 - W pliku `utils.py` znajdują się funkcje pomocnicze używane do rozwiązania zadań z listy - głównie rysujące wykresy.

# Zadanie 5

 - **a)** Obecność powtórzeń nie powinna mieć wpływu na warotość $\hat{n}$, jeśli używana funkcja haszująca spełnia warunek mówiący o tym, że funkcja haszująca zawsze powinna zwracać tą samą wartość dla tego smego argumentu. 

 - **b)** Wykres dla zbioru składającego się z losowych wartości z zakresu $[0, 2^{32})$:
    ![MinCount random data all](./mc_random/mc_all_random.png)
    dla k = 2:
    ![MinCount random data](./mc_random/2.png)
    dla k = 3:
    ![MinCount random data](./mc_random/3.png)
    dla k = 10:
    ![MinCount random data](./mc_random/10.png)
    dla k = 100:
    ![MinCount random data](./mc_random/100.png)
    dla k = 400:
    ![MinCount random data](./mc_random/400.png)

 - **c)** Przeprowadzono testy dla różnych wartości $k$ (wykres poniżej) i zauważono, że w okolicach $k = 200$ wynik osiągnął wystarczająco bliski dokładnemu wynik w 95% przypadków. Dla $k = 250$ i większych estymowana wartość była wystarczająco dokładna dla 100% przypadków (testy na zbiorach o liczności od 1 do 10000 elementów).
  ![...](./5_c.png)
  Wykres pokazuje ile 


# Zadanie 6

Przetestowano działanie algorytmu **MinCount** dla różnych funkcji haszujących, ich definicje znajdują się w pliku `hash_functions.py`. Algorytm zwraca dobre rezultaty dla funkcji, które:
 - są odporne na kolizje, tzn. jest małe prawdopodobieństwo, że dla kilku różnych wartości $x$ wartość $h(x)$ będzie taka sama.
 - równomiernie "wypełniają" zbiór wartości funkcji - chcemy, żeby zbiór $\{h(x_1), h(x_2), \dots, h(x_n)\}$ wyglądał jak zbiór losowych wartości.

Przykładowe funkcje, dla których rezultaty były widocznie gorsze(testowano dla 32-bitowych $x$):
 - $h_1(x) = <x_1, x_2, \dots, x_{10}>_2$ # (bierzemy 10 najbardziej znaczących bitów $x$)
 - $h_2(x) = x \mod(2^{16})$

Obie z tych funkcji nie były odporne na kolizje, dla wartości $x \in [0, 2^{32})$

Porównanie wyników dla "dobrej" funkcji i określonej wyżej $h_1$:
  ![MMinCount random data](./mc_hashes.png)

# Zadanie 7

Wykresy dla różnych wartości $\alpha$ i nierówności Czebyszewa:

 - $\alpha = 0.5\%$
  ![...](./7_chebyshev__b.png)
 - $\alpha = 1\%$
  ![...](./7_chebyshev_1__b.png)
 - $\alpha = 5\%$
  ![...](./7_chebyshev_5__b.png)

Wykresy dla różnych wartości $\alpha$ i nierówności Chernoffa:

  - TODO

# Zadanie 8

Implementacja algorytmu **HyperLogLog** znajduje się w pliku `hyper_log_log.py`.

Definicje funkcji haszujących wykorzystanych w testach znajdują się w pliku `hash_functions.py` i mają w nazwie prefiks "hyper".

Prezentacja wyników dla różnych wartości parametru $m$:
  ![HyperLogLog random data all](./hll_random/hll_all_random.png)
$m = 2^{6}$:
  ![HyperLogLog random data 6](./hll_random/64.png)
$m = 2^{12}$:
  ![HyperLogLog random data 12](./hll_random/4096.png)
$m = 2^{16}$:
  ![HyperLogLog random data 16](./hll_random/65536.png)



Porównanie algorytmów HyperLogLog i MinCount dla podobnej ilości używanej pamięci. 
Zakładamy, że rejestr zajmuje 5 bitów, a pojedynczy hash 32 bity.

 - ~80 bitów pamięci:
  ![Comp4](./comp/4.png)
 
 - ~320 bitów pamięci:
  ![Comp6](./comp/6.png)
 
 - ~10240 bitów pamięci:
  ![Comp11](./comp/11.png)

 - ~327680 bitów pamięci:
  ![Comp16](./comp/16.png)

Można zauważyć, że HyperLogLog radzi sobie trochę gorzej niż MinCount w momencie kiedy ma do dyspozycji bardzo mało pamięci. Widzimy też że poprawa dokładności wraz ze wzrostem używanej pamięci jest dużo większa w przypadku HyperLogLog niż w przypadku MinCount. Już dla 320 bitów HyperLogLog przybliża $n$ z błędem podobnym do MinCount, a kiedy ilość pamięci jest większa radzi sobie znacznie lepiej.
