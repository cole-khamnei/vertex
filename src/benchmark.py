import os
import sys

import subprocess
import psutil
import time

from memory_profiler import memory_usage

VERTEX_DIR = os.path.dirname(os.path.abspath(__file__)) + "/../"
TESTS_DIR = f"{VERTEX_DIR}/tests"
sys.path.insert(0, VERTEX_DIR)

import vertex

from tqdm.auto import tqdm

# ----------------------------------------------------------------------------# 
# ---------------            System Info Collection            ---------------# 
# ----------------------------------------------------------------------------# 

import platform, socket, re, uuid, json, psutil, logging

import cpuinfo


def get_cpu_info():
    """ """

    name = cpuinfo.get_cpu_info()["brand_raw"]
    cores = cpuinfo.get_cpu_info()["count"]

    return f"{name} {cores}-core"


def getSystemInfo():
    """ """
    try:
        info={}
        info['platform']=platform.system()
        info['platform-release']=platform.release()
        info['platform-version']=platform.version()
        info['architecture']=platform.machine()
        info['hostname']=socket.gethostname()
        info['ip-address']=socket.gethostbyname(socket.gethostname())
        info['mac-address']=':'.join(re.findall('..', '%012x' % uuid.getnode()))
        info['processor']=platform.processor()
        info['ram']=str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
        return info
        # return json.dumps(info)
    except Exception as e:
        logging.exception(e)

# json.loads(getSystemInfo())


# ----------------------------------------------------------------------------# 
# ---------------            Benchmarking Functions            ---------------# 
# ----------------------------------------------------------------------------# 


def sparse_correlation_task():
    """ """
    cifti_path = f"{TESTS_DIR}/sample_data/random.dtseries.nii"
    save_path = f"{TESTS_DIR}/outputs/example_vFC.npz"
    arg_list = f"-c {cifti_path} -o {save_path} -d auto"
    vertex.main(arg_list.split())


def pair_correlation_task():
    """ """
    cifti_path = f"{TESTS_DIR}/sample_data/random.dtseries.nii"
    save_path = f"{TESTS_DIR}/outputs/example_vFC.npz"
    arg_list = f"-m compare -c {cifti_path} -c2 {cifti_path} -o {save_path} -d auto"
    vertex.main(arg_list.split())


# def wb_dconn():
#     cifti_path = f"{TESTS_DIR}/sample_data/random.dtseries.nii"
#     dconn_path = f"{TESTS_DIR}/outputs/random.dconn.nii"
#     dconn_path = f"~/_tmp/random.dconn.nii"
#     cmd = ["wb_command", "-cifti-correlation", cifti_path, output_dconn]
#     subprocess.run(cmd, check=True)


def wb_dconn_task():
    cifti_path = f"{TESTS_DIR}/sample_data/random.dtseries.nii"
    dconn_path = f"{TESTS_DIR}/outputs/random.dconn.nii"
    dconn_path = f"/Users/cole/_tmp/random.dconn.nii"
    cmd = ["wb_command", "-cifti-correlation", cifti_path,
           dconn_path, "-mem-limit", "8"]
    subprocess.run(cmd, check=True)


def wb_pair_correlation_task():
    output_path = f"{TESTS_DIR}/outputs/wb_pair_corr.dscalar.nii"
    dconn_path = f"/Users/cole/_tmp/random.dconn.nii"
    cmd = ["wb_command", "-cifti-pairwise-correlation", dconn_path, dconn_path,
           output_path]
    subprocess.run(cmd, check=True)


def resource_monitor(task_func):
    """ """
    start_time = time.time()
    mem_usage = memory_usage(task_func, max_usage=True)
    elapse_time = time.time() - start_time

    return elapse_time, mem_usage


def benchmark_machine(n_trials=5):
    """ """

    system_benchmarks = {}
    system_benchmarks["system_info"] = get_cpu_info().replace(" ", "_")

    tasks = [pair_correlation_task, sparse_correlation_task]
    # tasks = [wb_pair_correlation_task]

    pbar = tqdm(tasks, desc="Running Tasks")
    pbar.update(0)
    for task in tasks:
        task_name = task.__name__.replace("_task", "")
        pbar.set_description(f"Running Tasks - {task_name}")
        task_stats = {"task": task_name}

        task_recordings = [resource_monitor(task) for _ in range(n_trials)]
        task_stats["elapsed_times"] = [t[0] for t in task_recordings]
        task_stats["mem_usages"] = [t[1] for t in task_recordings]

        system_benchmarks[task_name] = task_stats
        pbar.update(1)

    system_name = system_benchmarks["system_info"].lower()
    benchmark_file = f"{VERTEX_DIR}/benchmarks/{system_name}_benchmark.json"
    
    with open(benchmark_file, "w") as file:
        json.dump(system_benchmarks, file)


# ----------------------------------------------------------------------------# 
# --------------------                Main                --------------------# 
# ----------------------------------------------------------------------------# 

if __name__ == "__main__":

    
    # mem_usage = memory_usage(my_function)
    # elapse_time, mem_usage = resource_monitor(sparse_correlation_task)

    benchmark_machine()
    # print(f"Time Elapsed:{elapsed_time}\nMemory usage (MB): {mem_usage}")


# ----------------------------------------------------------------------------# 
# --------------------                End                 --------------------# 
# ----------------------------------------------------------------------------#
