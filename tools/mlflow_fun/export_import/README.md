# mlflow-fun/tools/export_import

Utilities to export and import MLflow experiments and runs.

## Overview

* Experiments
  * Export an experiment and all its runs to file system - directory or zip file
  * Import an experiment from file system - directory or zip file
  * Copies an experiment directly from one tracking server to another
* Runs
  * Export a run to file system - directory or zip file
  * Import a run from file system directory or zip file
  * Copies a run directly from one tracking server to another

### Common arguments 

`output` - can either be a directory or zip file (determined if `output` has a zip extension).

`log_source_info` creates metadata tags with expert information.  Example:
```
Name                         Value
mlflow_tools.timestamp       1551037752
mlflow_tools.timestamp_nice  2019-02-24 19:49:12
mlflow_tools.experiment_id   2368826
mlflow_tools.run_id          50fa90e751eb4b3f9ba9cef0efe8ea30
mlflow_tools.tracking_uri    http://localhost:5000
```

## Experiments

Coming soon.

## Runs

### Export run

Exports a run to file system.

```
python export_run.py \
  --run_id 50fa90e751eb4b3f9ba9cef0efe8ea30 \
  --output=out
  --log_source_info
```

Produces a directory with following structure:
```
run.json
artifacts
  plot.png
  sklearn-model
    MLmodel
    conda.yaml
    model.pkl
```
Sample run.json
```
{   
  "info": {
    "run_id": "130bca8d75e54febb2bfa46875a03d59",
    "experiment_id": "2",
    ...
  },
  "params": {
    "max_depth": "16",
    "max_leaf_nodes": "32"
  },
  "metrics": {
    "mae": 0.5845562996214364,
    "r2": 0.28719674214710467,
  },
  "tags": {
    "mlflow.source.git.commit": "a42b9682074f4f07f1cb2cf26afedee96f357f83",
    "mlflow.runName": "demo.sh",
    "run_origin": "demo.sh",
    "mlflow.source.type": "LOCAL",
    "mlflow_tools.export.tracking_uri": "http://localhost:5000",
    "mlflow_tools.export.timestamp": 1563572639,
    "mlflow_tools.export.timestamp_nice": "2019-07-19 21:43:59",
    "mlflow_tools.export.run_id": "130bca8d75e54febb2bfa46875a03d59",
    "mlflow_tools.export.experiment_id": "2",
    "mlflow_tools.export.experiment_name": "sklearn_wine"
  }
}
```

### Import run

Imports a run from a file system directory or zip file.
```
python import_run.py \
  --run_id 50fa90e751eb4b3f9ba9cef0efe8ea30 \
  --input=out \
  --experiment_name sklearn_wine2
```

### Copy run from one tracking server to another

Exports a run from one MLflow tracking server and imports it into another server.

In this example we use:

* Experiment [../../../examples/sklearn/wine-quality](../../../examples/sklearn/wine-quality)
* Source tracking server runs on port 5000 
* Destination tracking server runs on 5001

**Export and import the run**

Run [export_import_run.py](export_import_run.py). 

```
export MLFLOW_TRACKING_URI=http://localhost:5000

python export_import_run.py \
  --src_run_id 50fa90e751eb4b3f9ba9cef0efe8ea30 \
  --dst_experiment_id_name my_experiment \
  --dst_uri http://localhost:5001
  --log_source_info
```


**Check predictions from new run**

Check the predictions from the new run in the destination server.

```
export MLFLOW_TRACKING_URI=http://localhost:5001
cd ../../../examples/sklearn/wine-quality
python scikit_predict.py bf3890a927fb4c82be37221eed8069d7
```