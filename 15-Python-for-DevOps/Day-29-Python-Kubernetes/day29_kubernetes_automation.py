#!/usr/bin/env python3

# ==========================================
# Day 29 Practice: Python + Kubernetes Automation
# Scenario: Complete Kubernetes DevOps CLI
# Requirements: pip install kubernetes
# ==========================================

import sys
import logging

try:
    from kubernetes import client, config
    from kubernetes.client.rest import ApiException
except ImportError:
    print("FATAL: The 'kubernetes' python package is not installed. Run: pip install kubernetes")
    sys.exit(1)

logging.basicConfig(level=logging.INFO, format="%(message)s")


def init_kubernetes():
    """Authenticates with the cluster (handles both local and in-pod scenarios)."""
    try:
        config.load_kube_config()
    except Exception:
        try:
            config.load_incluster_config()
        except Exception as e:
            logging.critical("FATAL: Could not load kubeconfig or incluster config: %s", e)
            sys.exit(1)


# ==========================================
# 1. CLUSTER HEALTH CHECKER
# ==========================================
def cluster_health_sweep():
    """Scans ALL namespaces and reports any Pod that isn't Running or Succeeded."""
    v1 = client.CoreV1Api()
    logging.info("\n--- INITIATING CLUSTER-WIDE HEALTH SWEEP ---")
    
    try:
        pods = v1.list_pod_for_all_namespaces()
        unhealthy_pods = []
        
        for pod in pods.items:
            # We must inspect container_statuses to ensure the app is actually ready
            is_ready = False
            if pod.status.container_statuses:
                is_ready = all([c.ready for c in pod.status.container_statuses])
                
            if pod.status.phase not in ["Running", "Succeeded"] or not is_ready:
                unhealthy_pods.append({
                    "namespace": pod.metadata.namespace,
                    "name": pod.metadata.name,
                    "phase": pod.status.phase,
                    "ready": is_ready
                })
                
        if not unhealthy_pods:
            logging.info("SUCCESS: All pods across all namespaces are healthy and ready!")
            return
            
        logging.warning("WARNING: Found %s unhealthy/unready pods:", len(unhealthy_pods))
        print(f"{'NAMESPACE':<20} | {'POD NAME':<35} | {'PHASE':<15} | {'READY'}")
        print("-" * 80)
        for p in unhealthy_pods:
            print(f"{p['namespace']:<20} | {p['name']:<35} | {p['phase']:<15} | {str(p['ready'])}")
            
    except ApiException as e:
        logging.error("K8s API Error during health sweep: %s", e)


# ==========================================
# 2. DEPLOYMENT SCALER
# ==========================================
def scale_deployment(namespace: str, deployment_name: str, target_replicas: int):
    """Safely scales a deployment up or down."""
    apps_v1 = client.AppsV1Api()
    logging.info(f"\n--- SCALING DEPLOYMENT: {namespace}/{deployment_name} ---")
    
    try:
        # Fetch current state
        deployment = apps_v1.read_namespaced_deployment(name=deployment_name, namespace=namespace)
        current_replicas = deployment.spec.replicas
        
        if current_replicas == target_replicas:
            logging.info("Deployment is already at %s replicas. No action needed.", target_replicas)
            return
            
        logging.info("Scaling from %s -> %s replicas...", current_replicas, target_replicas)
        
        # Modify and Patch
        deployment.spec.replicas = target_replicas
        apps_v1.patch_namespaced_deployment(name=deployment_name, namespace=namespace, body=deployment)
        
        logging.info("Scale command successfully issued to API Server!")
        
    except ApiException as e:
        if e.status == 404:
            logging.error("Deployment '%s' not found in namespace '%s'.", deployment_name, namespace)
        else:
            logging.error("K8s API Error: %s - %s", e.status, e.reason)


# ==========================================
# 3. POD LOG ANALYZER
# ==========================================
def analyze_pod_logs(namespace: str, pod_name: str):
    """Fetches pod logs and automatically detects ERROR or FATAL signatures."""
    v1 = client.CoreV1Api()
    logging.info(f"\n--- ANALYZING LOGS: {namespace}/{pod_name} ---")
    
    try:
        logs = v1.read_namespaced_pod_log(name=pod_name, namespace=namespace)
        
        error_lines = []
        for line in logs.splitlines():
            # A simple heuristic for finding errors in standard application logs
            upper_line = line.upper()
            if "ERROR" in upper_line or "FATAL" in upper_line or "EXCEPTION" in upper_line:
                error_lines.append(line)
                
        if not error_lines:
            logging.info("No errors detected in the pod logs. Application appears stable.")
            return
            
        logging.warning("CRITICAL: Detected %s error signatures in logs!", len(error_lines))
        print("\n--- ERROR DUMP ---")
        for err in error_lines[-10:]: # Print last 10 errors
            print(err)
            
    except ApiException as e:
        if e.status == 404:
            logging.error("Pod '%s' not found in namespace '%s'.", pod_name, namespace)
        else:
            logging.error("K8s API Error: %s - %s", e.status, e.reason)


# ==========================================
# CLI ROUTER
# ==========================================
def main():
    if len(sys.argv) < 2:
        print("Usage: python day29_kubernetes_automation.py [command]")
        print("Commands:")
        print("  health                     - Scans entire cluster for broken pods")
        print("  scale <deploy> <replicas>  - Scales a deployment in the default namespace")
        print("  analyze <pod>              - Analyzes logs for a pod in the default namespace")
        sys.exit(1)
        
    init_kubernetes()
    command = sys.argv[1].lower()
    
    if command == "health":
        cluster_health_sweep()
        
    elif command == "scale":
        if len(sys.argv) != 4:
            print("Usage: python script.py scale <deployment_name> <number_of_replicas>")
            sys.exit(1)
        deploy_name = sys.argv[2]
        try:
            replicas = int(sys.argv[3])
            scale_deployment("default", deploy_name, replicas)
        except ValueError:
            print("ERROR: <number_of_replicas> must be an integer.")
            
    elif command == "analyze":
        if len(sys.argv) != 3:
            print("Usage: python script.py analyze <pod_name>")
            sys.exit(1)
        pod_name = sys.argv[2]
        analyze_pod_logs("default", pod_name)
        
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
