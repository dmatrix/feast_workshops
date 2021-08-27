
![](images/feast_logo.png)

### What is Feast?

[Feast](https://feast.dev/) is an operational data system for managing and serving machine learning features to 
models in production. It can serve features from a low-latency offline store (for real-time prediction) 
or from an off-line store (for scale-out batch scoring or training models).

![](images/feast_hero_010.png)
Feature stores have emerged as a pivotal component in the modern machine learning stack, as more data scientists 
and engineers work together to operationalize ML. Associated with this task are some operational challenges. 
The toughest challenges for operationalizing ML is data: how to compute and select features, store, 
validate serve, discover and share them.

### Goal and Objective
In this series of instructor led lectures and hands-on workshops, divided them into distinct modules, you will learn:

* what key problems feature stores solve to operationalize ML
* why features stores are a pivotal components in the model machine learning stack
* common key use cases and deployment patterns for feature stores observed by the MLOps and ML practitioners
* how feature stores are playing a transformational role with the rise of modern data platforms
* get a hands-on experience with the popular open source feature store Feast

The workshop, all done on your laptop, is divided into four modules:

|  Time (mins) |  Description |  Module |
|---|---|---|
| 45-60  | Feast Concepts, Declarative & Consumption APIs, and Creating Features for offline/online access | [Module 1](module_1/README.md)  |
| 45 | Quick intro to [MLflow](https://mlflow.org/) and Feast &  MLflow integration|[Module 2](module_2/README.md)  |
| 45  | Starting from scratch: A customer churn use case Linear Regression [XGBoost](https://xgboost.readthedocs.io/en/latest/) (WIP)  | [Module 3](module_3/README.md)   |
| 45  | How to use Feast on demand transformations (WIP)  | [Module 4](module_4/README.md)  |


### Who Should Take This Workshop

A data scientist or data engineer who wants to learn and understand: 
 * how Feature Store builds a bridge between your feature data and machine learning models
 * how to serve consistent features for both training and low-latency inference 
 * how to build feature engineering pipelines to build features

### Skill Level
Beginner to Intermediate

### Instructor

- [Jules S. Damji](https://www.linkedin.com/in/dmatrix/) 
- [@2twitme](https://twitter.com/2twitme)
     
### Prerequisites
 * Knowledge of Python 3 and programming in general
 * Preferably a UNIX-based, fully-charged laptop with 8-16 GB, with a Chrome or Firefox browser
 * Some knowledge of Machine Learning concepts, libraries, and frameworks:
   * scikit-learn
   * pandas and Numpy
   * PyCharm/IntelliJ or choice of syntax-based Python editor
 * pip/pip3 or conda and Python 3 installed
 * Loads of virtual laughter, curiosity, and a sense of humor ... :-)

### Obtaining the Workshop materials
Familiarity with **git** is important so that you can get all the material easily during the tutorial and
workshop as well as continue to work in your free time, after the session is over.

``` git clone git@github.com:dmatrix/feast_workshops.git```

``` git clone https://github.com/dmatrix/feast_workshops.git```

### Documentation Resources
This tutorial will refer to documentation:
 * [Feast Docs](https://rtd.feast.dev/en/latest/)
 * [Feast Python SDK](https://rtd.feast.dev/en/latest/)
 * [Feast CLI](https://docs.feast.dev/reference/feast-cli-commands)
