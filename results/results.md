# ltsconvert

| Directory                 | failures-divergence | impossible-futures | trace-ac        | weak-failures   | weak-trace-ac   |
| ------------------------- | --------------- | --------------- | --------------- | --------------- | --------------- |
| cases/coarseSet           |       3.820254s |       7.494300s |       0.203578s |       3.847069s |       3.811714s |
| cases/fineGrainedSet      |       0.202303s |       0.404298s |       0.103035s |       0.202308s |       0.202258s |
| cases/lazySet             |       0.505425s |       1.512022s |       0.102340s |       0.505509s |       0.504875s |
| cases/optimisticSet       |       6.442601s |      26.109786s |       0.303601s |       6.380432s |       6.436068s |
| cases/pracNonBlock        |       0.102323s |       0.102238s |       0.101704s |       0.102205s |       0.102060s |
| cases/treiberStack        |     149.390872s |     345.811756s |       0.404231s |     150.047570s |     148.839408s |

# merc-lts

| Directory                 | failures-divergences | impossible-futures | stable-failures | trace           | weaktrace       |
| ------------------------- | --------------- | --------------- | --------------- | --------------- | --------------- |
| cases/coarseSet           |       0.786829s |       1.475860s |       0.605316s |       0.102552s |       0.605551s |
| cases/fineGrainedSet      |       0.102373s |       0.102530s |       0.101881s |       0.102705s |       0.102110s |
| cases/lazySet             |       0.202785s |       0.202917s |       0.101656s |       0.102143s |       0.101649s |
| cases/optimisticSet       |       4.571852s |       2.105677s |       1.315009s |       0.161907s |       1.334215s |
| cases/pracNonBlock        |       0.102612s |       0.102086s |       0.101624s |       0.102415s |       0.102209s |
| cases/treiberStack        |      32.579314s |      47.897847s |      20.550114s |       0.202449s |      20.521728s |