""" 
Exports a run from one MLflow server and imports it into another server. 
First create an experiment in the destination MLflow server: mlflow experiments create my_experiment
"""

from __future__ import print_function

import os
import time
import datetime
import shutil
from argparse import ArgumentParser
import mlflow
from mlflow import tracking

def run(src_run_id, dst_exp_id, dst_uri, log_source_info):
    print("src_run_id:",src_run_id)
    print("dst_exp_id:",dst_exp_id)
    print("dst_uri:",dst_uri)
    print("log_source_info:",log_source_info)

    src_client = mlflow.tracking.MlflowClient()
    src_uri = mlflow.tracking.get_tracking_uri()
    src_run = src_client.get_run(src_run_id)

    dst_client = mlflow.tracking.MlflowClient(dst_uri)
    dst_exp = dst_client.get_experiment(dst_exp_id)
    print("dst_exp:",dst_exp)
    
    mlflow.tracking.set_tracking_uri(dst_uri)
    with mlflow.start_run( \
            experiment_id=dst_exp.experiment_id, \
            run_name=src_run.info.name, \
            source_name=src_run.info.source_name, \
            source_version=src_run.info.source_version, \
            source_type=src_run.info.source_type, \
            entry_point_name=src_run.info.entry_point_name \
            # nested=src_run.info.nested # NOTE: where is nested flag?
            ) as run:
        dst_run_id = run.info.run_uuid
        print("dst_run_id:",dst_run_id)
        for e in src_run.data.params:
             mlflow.log_param(e.key, e.value)
        for e in src_run.data.metrics:
             mlflow.log_metric(e.key, e.value)
        for e in src_run.data.tags:
             mlflow.set_tag(e.key, e.value)

        if log_source_info:
             mlflow.set_tag("_exim_src_run_id",src_run_id)
             mlflow.set_tag("_exim_src_experiment_id",src_run.info.experiment_id)
             mlflow.set_tag("_exim_src_uri",src_uri)
             dbx_host = os.environ.get("DATABRICKS_HOST",None)
             if dbx_host is not None:
                 mlflow.set_tag("_exim_DATABRICKS_HOST", dbx_host)
             now = int(time.time()+.5)
             snow = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(now))
             mlflow.set_tag("_exim_import_timestamp",now)
             mlflow.set_tag("_exim_import_timestamp_nice",snow)

        # copy artifacts
        local_path = src_client.download_artifacts(src_run_id,"")
        print("local_path:",local_path)
        mlflow.log_artifacts(local_path)
        shutil.rmtree(local_path)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--src_run_id", dest="src_run_id", help="Source run_id", required=True)
    parser.add_argument("--dst_uri", dest="dst_uri", help="Destination MLFLOW API URL", required=True)
    parser.add_argument("--dst_experiment_id", dest="dst_experiment_id", help="Destination experiment_id", required=True, type=int)
    parser.add_argument("--log_source_info", dest="log_source_info", help="Set tags with import information", default=False, action='store_true')
    args = parser.parse_args()
    run(args.src_run_id, args.dst_experiment_id, args.dst_uri, args.log_source_info)