# Fraud Detection Platform

An end-to-end MLOps platform that monitors a credit-card fraud model for drift, trains a replacement when drift is detected, and deploys it only after a person approves each step. The full cloud setup, including an AWS emulator, a Kubernetes cluster, and CI/CD, runs locally in Docker with a single `make up`.

**Stack:** Python 3.12, Apache Airflow, MLflow, XGBoost, Optuna, Evidently, FastAPI, PostgreSQL, Terraform, Kubernetes (K3s), GitHub Actions, Docker, Atlas, Slack

## At a glance

| Area | Summary |
|---|---|
| Orchestration | 4 Airflow DAGs coordinate cold-start seeding, daily drift checks, training, and promotion. |
| Model | XGBoost classifier tuned with Optuna and registered in MLflow, scoring 0.874 PR-AUC and 0.800 F1 on a held-out split. |
| Serving | FastAPI service on Kubernetes that loads the active model from MLflow and stores every prediction in PostgreSQL. |
| Human-in-the-loop | Slack approvals gate both training and promotion. |
| Infrastructure | 18 Terraform modules provision emulated AWS services (S3, ECR, RDS, EKS, MWAA, Secrets Manager, SSM), MLflow, Traefik, MetalLB, and Kyverno. |
| CI/CD | 6 GitHub Actions workflows run locally with act, covering image builds, DAG sync, API deployment, and schema migrations. |
| Tests | 194 test functions across 102 files covering the DAGs, job images, shared code, and the API, run inside Docker image builds. |

## How it works

### Architecture

Airflow runs each heavy step as a Kubernetes pod. Slack approvals reach the API over Socket Mode, and the API triggers the matching DAG through the MWAA REST API.

### Model lifecycle

| DAG | Trigger | What it does |
|---|---|---|
| `cold_start` | `make up` | Creates the project row, seeds `transaction_inferences` from S3 when the table is empty, then runs `check_training_need`. |
| `check_training_need` | Daily | Expires stale challengers, runs the drift-check pod, and posts a Slack approval request when training is needed. |
| `on_training_decision` | Slack button | Trains the model in a pod after approval, registers it in MLflow, and posts a promotion request. |
| `on_promotion_decision` | Slack button | Marks the new model as the active deployment, dispatches the API deploy workflow, and archives old inferences to S3. |

## Model results

Results come from the notebook experiments in [`notebooks/02_models.ipynb`](notebooks/02_models.ipynb). Each model is a RobustScaler, SMOTE, and classifier pipeline tuned by Optuna with up to 30 trials and a 1-hour limit, then scored on a stratified 20% split (56,962 test rows, 492 frauds in the full dataset).

| Model | F1 | PR-AUC | Recall | Precision |
|---|---|---|---|---|
| KNN | 0.256 | 0.647 | 0.929 | 0.148 |
| Random Forest | 0.720 | 0.857 | 0.878 | 0.610 |
| **XGBoost** | **0.800** | **0.874** | 0.857 | **0.750** |
| MLP (PyTorch) | 0.612 | 0.835 | 0.878 | 0.470 |

XGBoost scored highest on PR-AUC, so it is the model the platform use. SHAP interpretation is in [`notebooks/03_model_interpretation.ipynb`](notebooks/03_model_interpretation.ipynb).

## Design decisions

| Decision | Implementation |
|---|---|
| Two approval gates | Slack buttons gate training and promotion, so no model trains or ships without a person. Newer requests invalidate older approval messages, and an unpromoted challenger expires after 7 days. |
| Workflow state in PostgreSQL | `model_deployment_workflows` stores the state (`train_pending`, `promote_pending`, `reserved`) behind a CHECK constraint, and a partial unique index allows only 1 active deployment per project. |
| Two drift signals | Evidently's data-drift preset compares feature distributions, and an F1 drop of 0.05 or more against the model's reference dataset flags concept drift. Classification metrics are computed only with 100,000+ labeled rows. |
| Imbalance-aware training | RobustScaler, SMOTE, and XGBoost with `scale_pos_weight`, tuned by Optuna using 4-fold stratified cross-validation on average precision. |
| Failed runs leave no trace | A transactional MLflow run deletes the run and its model versions when training fails. |
| Jobs as pods | Drift check, training, archive, and seeding run as Kubernetes pods from ECR images, and CD updates each image reference through Airflow Variables stored in Secrets Manager. |
| Cloud parity on one machine | MiniStack emulates the AWS APIs, K3s backs the EKS cluster, and a small FastAPI shim answers GitHub's workflow-dispatch endpoint so a promotion can trigger the API deployment locally. |
| Team isolation | Each team gets a Kubernetes namespace, a PostgreSQL schema with roles, and an MLflow workspace, while Kyverno policies block non-admin edits to platform ConfigMaps and Secrets. |
| Safe schema changes | Atlas lints migrations in CI and treats destructive or backward-incompatible changes as errors. |
| Bounded inference storage | After each promotion, older inferences move to S3 as Parquet files with Hive-style date partitions in 50,000-row batches. |

## Where to look

| Area | Path | Contents |
|---|---|---|
| DAGs | [`dags/dags/model_lifecycle_orchestrator/`](dags/dags/model_lifecycle_orchestrator/) | The 4 DAGs with task, repository, controller, and schema modules. |
| Drift check | [`services/dags_images/drift_check/`](services/dags_images/drift_check/) | Evidently reports, reference and current dataset loaders, and S3 report upload. |
| Training | [`services/dags_images/train_model/`](services/dags_images/train_model/) | Optuna search space, pipeline, evaluation, and MLflow registration. |
| Archival and seeding | [`services/dags_images/archive/`](services/dags_images/archive/), [`services/dags_images/seed_transaction_inferences/`](services/dags_images/seed_transaction_inferences/) | Parquet archival to S3 and CSV seeding into PostgreSQL. |
| Inference API | [`services/fraud_detection_api/`](services/fraud_detection_api/) | FastAPI app, Slack handlers, MWAA trigger, and Kubernetes manifests. |
| Shared code | [`services/shared/`](services/shared/) | Configs, ORM models, and MLflow, S3, and PostgreSQL helpers. |
| Infrastructure | [`infrastructure/`](infrastructure/) | 18 Terraform modules and the tooling image. |
| CI/CD | [`.github/`](.github/) | 6 workflows, composite actions, and the act image. |
| Migrations | [`database/`](database/) | Atlas config and the initial PostgreSQL schema. |
| Experiments | [`notebooks/`](notebooks/) | EDA, 4-model comparison, and SHAP interpretation. |
| Make targets | [`makefiles/`](makefiles/) | Bash and PowerShell scripts behind every `make` command. |

## Run it locally

### Prerequisites

- Docker with `docker run --use-api-socket` support.
- GNU Make, uv, and the Atlas CLI on the host, because `make up` refreshes the lockfiles and the migration hash locally.
- Bash on Linux and macOS, or PowerShell on Windows.
- A Slack app (app-level token, bot token, signing secret, and channel ID) for the approval flow.
- The seed file `database/seed/transaction_inferences/creditcard_transactions.csv.gz`, a gzip CSV with `Time`, `V1` to `V28`, `Amount`, and `Class` columns.

### Steps

1. Copy `.env.example` to `.env`, `.secrets.example` to `.secrets`, and `infrastructure/terraform.tfvars.example` to `infrastructure/terraform.tfvars`.
2. Fill in the Slack values and a GitHub token in `.secrets`. The AWS and database values are local placeholders for the emulator.
3. Run `make up`.

`make up` runs these stages in order: refresh the lockfiles and the Atlas hash, provision the infrastructure with Terraform inside a container, apply the schema migration, push the job images and sync the DAGs, and trigger the `cold_start` DAG. `make init` is optional and creates local virtual environments for editing with `uv sync`.

Terraform prints the service URLs as outputs (`ministack_host_url`, `mlflow_host_url`, and `mwaa_teams_host_urls`).

| Service | URL |
|---|---|
| MiniStack (emulated AWS) | `http://localhost:4566` |
| MLflow | `http://mlflow.127.0.0.1.sslip.io` |
| Inference API (after the first promotion) | `http://fraud-detection-api.127.0.0.1.sslip.io` |
| Airflow | The localhost URL in the `mwaa_teams_host_urls` output |

| Command | What it runs |
|---|---|
| `make test-dags` | The DAG CI workflow with act on a pull-request event. |
| `make test-fraud-detection-api` | The API CI workflow. |
| `make test-migration` | The migration CI workflow with Atlas lint. |
| `make deploy-dags`, `make deploy-fraud-detection-api`, `make deploy-migration` | The matching CD workflow with act on a push event. |
| `make down` | Destroys the infrastructure. |

## Tests and CI

- Each Dockerfile has a `test` target that runs pytest during the build, so a failing test fails CI.
- DAG tests load every DAG with `DagBag` and assert no import errors, no cycles, and a failure callback.
- Migration CI starts a throwaway `postgres:15-alpine` service and runs `atlas migrate lint`.
- Path filters rebuild only the images whose folders, shared code, or lockfile changed.

## Scope and limits

- The platform runs on emulators (MiniStack and K3s) and has not been deployed to real AWS. A few MiniStack workarounds are documented in the Terraform comments.
- Credentials in the example files are development placeholders.
- DAGs reach the Airflow container through `docker exec` and rsync, because the S3-based MWAA DAG upload does not work in this setup.
- There is no hosted demo, since the platform needs the local stack.
- One team, `mle`, is defined in [`infrastructure/locals.tf`](infrastructure/locals.tf).

## Data

The notebooks, seed loader, and model features follow the layout of the public [ULB credit card fraud dataset on Kaggle](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud): 284,807 transactions, 492 labeled frauds, 28 anonymized PCA features (`V1` to `V28`), `Time`, `Amount`, and `Class`. The seed loader maps `Time` to timestamps starting at 2013-09-01 UTC.

## Author

Built by Reaven Dupitas ([@u-Kuro](https://github.com/u-Kuro)).
