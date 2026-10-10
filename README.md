# Fraud Detection Platform

An end-to-end MLOps platform that monitors a credit-card fraud model for drift, trains a replacement when drift is detected, and deploys it only after a person approves each step. The full cloud setup, including an AWS emulator, a Kubernetes cluster, and CI/CD, runs locally in Docker with a single `make up`.

**Stack:** Python 3.12, Apache Airflow, MLflow, XGBoost, scikit-learn, Optuna, Evidently, FastAPI, PostgreSQL, Terraform, Kubernetes (K3s), GitHub Actions (nektos/act), Docker, Atlas (ariga/atlas), Slack

## At a glance

| Area | Summary |
|---|---|
| Orchestration | 4 Airflow DAGs coordinate cold-start seeding, daily drift checks, training, and promotion. |
| Model | XGBoost classifier tuned with Optuna and registered in MLflow, scoring 0.866 PR-AUC and 0.761 F1 on a held-out split. |
| Serving | FastAPI service on Kubernetes that loads the active model from MLflow, flags fraud above a 0.875 probability cutoff, and stores every prediction in PostgreSQL. |
| Human-in-the-loop | Slack approvals gate both training and promotion. |
| Infrastructure | 19 Terraform modules provision emulated AWS services (S3, ECR, RDS, EKS, MWAA, IAM, Secrets Manager, SSM), MLflow, Traefik, MetalLB, Kyverno, and the supporting containers. |
| CI/CD | 6 GitHub Actions workflows run locally with nektos/act, covering image builds, DAG sync, API deployment, and schema migrations. |
| Tests | 183 test functions across 96 files covering the DAGs, job images, shared code, and the API, run inside Docker image builds. |
| Screenshots | Airflow, MLflow, and the inference API from a local run, linked in "Screenshots" below. |
| Run it | `make up` provisions and starts everything locally. Steps are in "Run it locally" below. |

## How it works

### Components

| Layer | Components | Role |
|---|---|---|
| Orchestration | Airflow with 4 DAGs | Schedules the drift check, runs each job as a Kubernetes pod, and posts Slack approval requests. |
| Workloads | K3s cluster standing in for EKS | Runs the 4 job images (drift check, training, archive, seed) and the FastAPI inference service. |
| Serving | FastAPI service | Loads the active model from MLflow, serves `/predict`, and stores each prediction in PostgreSQL. |
| Approvals | Local shim container | Receives Slack button clicks over Socket Mode and triggers the matching DAG through the MWAA API. |
| Tracking | MLflow on the cluster | Tracks experiments and registers models in per-team workspaces, backed by PostgreSQL and S3. |
| Data and images | MiniStack (emulated AWS) | Provides RDS PostgreSQL, S3, ECR, Secrets Manager, SSM, and IAM for workflow state, inferences, artifacts, reports, archives, and container images. |
| CI/CD | 6 GitHub Actions workflows run by act | Builds and pushes images, syncs DAGs, applies migrations, and deploys the API when a promotion dispatches the workflow. |

The shim container also answers GitHub's workflow-dispatch endpoint by running the requested workflow with act, so a promotion can trigger the API deployment locally.

### Model lifecycle

1. `cold_start` seeds `transaction_inferences` from S3 when the table is empty, then starts `check_training_need`.
2. `check_training_need` runs daily and, when a model is deployed, launches the drift-check pod.
3. When drift is detected or no model is deployed yet, a Slack message asks a person to approve training.
4. After approval, `on_training_decision` trains and registers the model in a pod, then posts a promotion request.
5. A person approves promotion in Slack.
6. `on_promotion_decision` records the model as the active deployment, dispatches the API deployment, and archives the inferences used for training to S3.

A rejected approval deletes the workflow, and a daily run without drift takes no action.

## Model results

Results come from the notebook experiments in [`notebooks/02_models.ipynb`](notebooks/02_models.ipynb). Each model is a pipeline of RobustScaler, SMOTE, and a classifier, tuned by Optuna with up to 30 trials and a 1-hour limit, then scored on a stratified 20% split (56,962 test rows, 492 frauds in the full dataset).

| Model | F1 | PR-AUC | Recall | Precision |
|---|---|---|---|---|
| KNN | 0.256 | 0.647 | 0.929 | 0.148 |
| Random Forest | 0.720 | 0.853 | 0.878 | 0.610 |
| **XGBoost** | **0.761** | **0.866** | 0.878 | **0.672** |
| MLP (PyTorch) | 0.427 | 0.836 | 0.867 | 0.283 |

XGBoost scored highest on F1, PR-AUC, and precision, and it is the model the platform trains. KNN reached the highest recall, but at a precision of 0.148. SHAP interpretation is in [`notebooks/03_model_interpretation.ipynb`](notebooks/03_model_interpretation.ipynb).

## Screenshots

Screenshots from a local run are in [`screenshots/`](screenshots/).

| Area | Screenshots |
|---|---|
| Airflow | [DAG list](screenshots/airflow-dag-runs.png) with the 4 DAGs and their latest successful runs. |
| MLflow training run | [Metrics](screenshots/mlflow-xgboost-run-metrics.png), [parameters](screenshots/mlflow-xgboost-run-parameters.png), and [artifacts](screenshots/mlflow-xgboost-run-artifacts.png) of the XGBoost run in the `mle` workspace. |
| MLflow model registry | [Version 1 of the `xgboost` model](screenshots/mlflow-xgboost-model-registry-version.png) with its input and output schema. |
| Evaluation plots | [Confusion matrix](screenshots/mlflow-xgboost-confusion-matrix.png) and [fraud probability scatter](screenshots/mlflow-xgboost-fraud-probability-scatter.png) logged by the training run. |
| Inference API | [Request](screenshots/fraud-detection-api-request.png) and [response](screenshots/fraud-detection-api-response.png) for `POST /predict` in the FastAPI docs. |

The MLflow metrics come from a training run of the platform itself, separate from the notebook experiments above.

## Design decisions

| Decision | Implementation |
|---|---|
| Two approval gates | Slack buttons gate training and promotion, so no model trains or ships without a person. Newer training requests invalidate older approval messages, and the daily DAG has a cleanup branch for challengers left unpromoted for 7 days. |
| Workflow state in PostgreSQL | `model_deployment_workflows` tracks each approval request with its Slack message timestamps and model run, a CHECK constraint restricts `state` to known values, and a partial unique index allows only 1 active deployment per project. |
| Two drift signals | Data drift uses Evidently's preset with PSI and triggers when 50% or more of the features drift or the prediction probability drifts. Concept drift triggers when average precision drops 0.1 or more against the model's reference dataset. |
| Row limits | Drift checks and training each need at least 100,000 labeled rows and read at most 500,000. Concept drift also needs 100 or more frauds in both datasets, so thin data does not trigger a training request. |
| Imbalance-aware training | The RobustScaler, SMOTE, and XGBoost pipeline is tuned by Optuna using 4-fold stratified cross-validation on average precision, with SMOTE applied inside each fold. |
| Failed runs leave no trace | A transactional MLflow run deletes the run and its model versions when training fails. |
| Jobs as pods | Drift check, training, archive, and seeding run as Kubernetes pods from ECR images, and CD updates each image reference through Airflow Variables stored in Secrets Manager. |
| Cloud parity on one machine | MiniStack emulates the AWS APIs, K3s stands in for EKS, and the shim container stands in for GitHub's workflow-dispatch endpoint. |
| Team isolation | Each team gets scoped IAM policies, a Kubernetes namespace, a PostgreSQL schema with roles, and an MLflow workspace, while Kyverno policies deny edits to the platform ConfigMap and Secrets by anyone outside the cluster-admin group. |
| Safe schema changes | Atlas lints migrations in CI and treats destructive or backward-incompatible changes as errors. |
| Bounded inference storage | After each promotion, the inferences used to train the promoted model move to S3 as Parquet files with Hive-style date partitions, in 50,000-row batches, and are deleted from PostgreSQL. |

## Tests and CI

- Each Dockerfile has a `test` target that runs pytest during the build, so a failing test fails CI.
- DAG tests load every DAG with `DagBag` and assert no import errors, no cycles, a failure callback, and unpaused creation.
- Migration CI starts a throwaway `postgres:15-alpine` service and runs `atlas migrate lint`.
- Path filters rebuild only the images whose folders, shared code, or lockfile changed.
- `make test` also runs `terraform validate` inside the tooling container.

## Scope and limits

- The platform runs on emulators (MiniStack and K3s) and has not been deployed to real AWS. A few MiniStack workarounds are documented in the Terraform comments.
- Credentials in the example files are development placeholders.
- DAGs reach the Airflow container using `docker cp` and rsync, because the S3-based MWAA DAG upload does not work in this setup.
- There is no hosted demo, since the platform needs the local stack.
- One team, `mle`, is defined in [`infrastructure/locals.tf`](infrastructure/locals.tf).

<details>
<summary><b>Where to look</b> (folder map)</summary>

| Area | Path | Contents |
|---|---|---|
| DAGs | [`dags/dags/model_lifecycle_orchestrator/`](dags/dags/model_lifecycle_orchestrator/) | The 4 DAGs with task, repository, controller, and schema modules. |
| Drift check | [`services/dags_images/drift_check/`](services/dags_images/drift_check/) | Evidently reports, reference and current dataset loaders, and S3 report upload. |
| Training | [`services/dags_images/train_model/`](services/dags_images/train_model/) | Optuna search space, pipeline, evaluation, and MLflow registration. |
| Archival and seeding | [`services/dags_images/archive/`](services/dags_images/archive/), [`services/dags_images/seed_transaction_inferences/`](services/dags_images/seed_transaction_inferences/) | Parquet archival to S3 and CSV seeding into PostgreSQL. |
| Inference API | [`services/fraud_detection_api/`](services/fraud_detection_api/) | FastAPI app, prediction storage, and Kubernetes manifests. |
| Slack and GitHub shim | [`infrastructure/modules/docker/shim/`](infrastructure/modules/docker/shim/) | Slack Socket Mode handlers, MWAA DAG triggers, and the workflow-dispatch endpoint that runs act. |
| Shared code | [`services/shared/`](services/shared/) | Configs, ORM models, and MLflow, S3, and PostgreSQL helpers. |
| Infrastructure | [`infrastructure/`](infrastructure/) | 19 Terraform modules and the tooling image. |
| CI/CD | [`.github/`](.github/) | 6 workflows, composite actions, and path filters. |
| Migrations | [`database/`](database/) | Atlas config and the initial PostgreSQL schema. |
| Experiments | [`notebooks/`](notebooks/) | EDA, 4-model comparison, and SHAP interpretation. |
| Make targets | [`makefiles/`](makefiles/) | Bash and PowerShell scripts behind every `make` command. |

</details>

<details>
<summary><b>Run it locally</b> (prerequisites, steps, URLs, commands)</summary>

### Prerequisites

- Docker with `docker run --use-api-socket` support.
- GNU Make, uv, the [ariga/atlas](https://github.com/ariga/atlas) CLI, and [nektos/act](https://github.com/nektos/act) on the host, since `make up` uses uv for the lockfiles, Atlas for the migration hash, and act for the migration and DAG deployment workflows.
- A git clone of this repository, since the DAG workflows need its commit history.
- Bash on Linux and macOS, or PowerShell on Windows.
- A GitHub [fine-grained personal access token](https://github.com/settings/personal-access-tokens) with read-only permissions for contents, metadata, and pull requests.
- A Docker Hub username and personal access token with read and write permissions.
- A Slack workspace where an app can be created, with a channel for approval requests.

### Steps

1. Create a Slack app, add the bot token scope `chat:write`, install it to the workspace, and copy the Bot User OAuth Token.
2. Turn on Socket Mode and generate an app-level token with the `connections:write` scope, so the approval buttons need no request URL.
3. Copy the signing secret from the app's Basic Information page, then add the bot to the channel that will receive approval requests and copy that channel's ID.
4. Copy `.env.example` to `.env`, `.secrets.example` to `.secrets`, and `infrastructure/terraform.tfvars.example` to `infrastructure/terraform.tfvars`.
5. Fill in the Slack tokens and signing secret in `.env` and `.secrets`, and add the channel ID, GitHub token, and Docker Hub credentials to `.secrets`. The AWS and database values are local placeholders for the emulator.
6. Start Docker and run `make up`.
7. Wait for the bot to post a "First Training Required" message in the channel after `make up` finishes, then click **Approve Training** to start the training pod.
8. After training finishes (the Optuna search stops at 30 trials or 1 hour), click **Approve Promotion** in the "Challenger Model Promotion Required" message, which shows the model's PR-AUC, F1, recall, and precision.
9. After the API deployment workflow completes, open the Inference API URL from the service table below and append `/docs` to try `POST /predict`.

`make up` runs these stages in order:

- Refresh the lockfiles and the Atlas hash on the host.
- Provision the infrastructure with Terraform inside a container.
- Apply the schema migration with act.
- Push the job images and sync the DAGs with act.
- Upload the seed file from `database/seed/transaction_inferences/` and trigger the `cold_start` DAG inside a container.

`make init` is optional and uses `uv sync` to create local virtual environments for editing.

After the first deployment, the daily check posts a new training request only when drift is detected. Any failed task posts a "Task Failed" message with a log link in the same channel.

Terraform prints the service URLs as outputs (`ministack_host_url`, `mlflow_host_url`, and `mwaa_teams_environment_host_urls`).

| Service | URL |
|---|---|
| MiniStack (emulated AWS) | `http://localhost:4566` |
| MLflow | `http://mlflow.127.0.0.1.sslip.io` |
| Inference API (after the first promotion) | `http://fraud-detection-api.127.0.0.1.sslip.io` |
| Airflow | The localhost URL in the `mwaa_teams_environment_host_urls` output |

Commands that run workflows with act execute on the host and join the stack's Docker network, so they need the infrastructure to be up first. The API deployment that a promotion triggers runs differently, since the shim starts it with act inside a container. `make format` and the `terraform validate` step of `make test` run in the tooling container and do not need the infrastructure.

| Command | What it runs |
|---|---|
| `make test` | `terraform validate` plus the 3 CI workflows. |
| `make test-dags` | The DAG CI workflow with act on a pull-request event. |
| `make test-fraud-detection-api` | The API CI workflow. |
| `make test-migration` | The migration CI workflow with Atlas lint. |
| `make deploy-dags`, `make deploy-fraud-detection-api`, `make deploy-migration` | The matching CD workflow with act on a push event. |
| `make format` | `terraform fmt` on the infrastructure folder. |
| `make down` | Destroys the infrastructure. |

</details>

## Data

The notebooks, seed loader, and model features follow the layout of the public [ULB credit card fraud dataset on Kaggle](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud): 284,807 transactions, 492 labeled frauds, 28 anonymized PCA features (`V1` to `V28`), `Time`, `Amount`, and `Class`. The seed loader maps `Time` to timestamps starting at 2013-09-01 UTC.

## Author

Built by Reaven Dupitas ([@u-Kuro](https://github.com/u-Kuro)).