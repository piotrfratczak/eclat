# eclat
Python implementation of ECLAT algorithm for association rule mining.

This implementation mines rules ![equation](https://latex.codecogs.com/svg.image?{\color{Emerald}a&space;\to&space;Ah}), such that
![equation](https://latex.codecogs.com/svg.image?{\color{Emerald}a}) is an element in a transaction and
![equation](https://latex.codecogs.com/svg.image?{\color{Emerald}Ah}) is an element in hierarchy that a belongs to.
This kind of rule is mined on the condition that there are transactions
![equation](https://latex.codecogs.com/svg.image?{\color{Emerald}t&space;:&space;t&space;\supset&space;(a,b),&space;&space;&space;a&space;\in&space;E(Ah),&space;&space;&space;b&space;\in&space;E(Ah)})
, where ![equation](https://latex.codecogs.com/svg.image?{\color{Emerald}E(y)}) is an itemset belonging to an element in hierarchy
![equation](https://latex.codecogs.com/svg.image?{\color{Emerald}y}).

## Setup
```shell
$ conda env create -f environment.yml
$ conda activate eclat
```

## Execution
Execute with default parameters:
```shell
$ python main.py
```

### Parameters

#### Predefined Datasets
To execute for a predefined dataset:
```shell
$ python main.py --dataset=<dataset_id>
```
Possible _dataset_id_ values:
* 0 - small debugging dataset,
* 1 - [FruitHut](http://www.philippe-fournier-viger.com/spmf/datasets/fruithut_original.txt) dataset,
* 2 - [Liquor11](http://www.philippe-fournier-viger.com/spmf/liquor_11frequent.txt) dataset.

#### Custom Dataset
To execute for a custom dataset:
```shell
$ python main.py --data=<path/to/transactions.txt> --taxonomy=<path/to/taxonomy.txt>
```
**File with taxonomy is optional. Rules based on hierarchy of items are not mined if taxonomy is not provided.**

Example of _transactions.txt_ file format:
> 1 2 3  
> 1 2  
> 1 3

Example of _taxonomy.txt_ file format:
> 1,11  
> 2,11  
> 3,22  
> 11,111  
> 22,111

#### ECLAT parameters
An example of execution with ECLAT parametrization:
```shell
$ python main.py --min_sup=5 --min_conf=0.8 --min_len=3 --max_len=10
```
The options are:
* _min_sup_ - minimum support of the base of mined rules (type=int, default=1),
* _min_conf_ - minimum confidence of mined rules (type=float, default=0.5),
* _min_len_ - minimum length of mined rules (type=int, default=1),
* _max_len_ - maximum length of mined rules (type=int, default=None - not limited by default).

## Unit Tests
To execute unit tests run the following command in the main directory:
```shell
$ python -m unittest test.test_eclat
```

## Experiments
To run efficiency experiments:
```shell
$ python -m test.test_efficiency
```