# Cloud deployment extension points

The credential-free demo runs locally or in any container platform. Production adapters are intentionally separated from the core workflow.

- **Azure:** Azure AI Foundry/Inference for models, Azure AI Search for vectors, Azure ML for tracked deployments, and AKS or Container Apps for runtime.
- **AWS:** Bedrock or SageMaker for model endpoints, OpenSearch for retrieval, CloudWatch/OpenTelemetry for telemetry, and EKS/ECS for runtime.
- **Google Cloud:** Vertex AI for models/evaluation, Vector Search for retrieval, Cloud Logging/OpenTelemetry for telemetry, and GKE/Cloud Run for runtime.
- **Databricks:** Spark/Delta ingestion, Unity Catalog governance, MLflow experiment tracking, and Model Serving for scalable inference.

Use workload identity/OIDC rather than long-lived cloud credentials in CI. Store secrets in the platform secret manager, not in Kubernetes ConfigMaps or repository files.
