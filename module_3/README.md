### A Credit Scoring Use Case for Loan Approval

#### Workshop Objective:

 * Load data and peruse the data
 * Declare and Define all Feast Primitives or First Class Objects (fco)
 * Feast apply
 * Feast materialize
 * Train model using XGBoost 
   * First using a single core
   * Use Ray to do distributed training on four cores
 * Get data from online store for credit score and loan approval 

![](images/feast_ray_xgboost.png)


### Setup and Installation

### Step 1:
Activate the conda environment used in Module 1. This should have all the packages
installed in module 1.

``` conda activate feast_workshop ```
### Step 2:
``` ray --version ```

### Step 3: Create the Feast Feature Store 
```cd cd <your_cloned_git_dir>/feast_workshops/module_3/queries```

```python create_feature_store.py```

### Step 4: Train the XGBoost program on a single core or process

```python train_model.py```

### Step 5: Train the XGBoost on Ray's distributed training using multiple cores or processes

```python ray_train_model.py```

![](images/ray_xgboost.png)

<hr style="border:3px solid gray"> </hr>

Alternatively, you could do all the above steps inside a Jupyter Notebook


```cd <your_cloned_git_dir>/feast_workshops/module_3/labs```

```jupyter lab```
