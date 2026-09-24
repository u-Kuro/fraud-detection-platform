# Do not remove.
# Reason: Apache Airflow adds "dags/" directory to sys.path instead of its parent, making "dags/" unresolvable as a package.
# Fix:    This file acts as the "dags" package, pointing Python to the "dags/" directory so imports like "from dags.x" work.
from pathlib import Path

dags_directory = Path(__file__).resolve().parent
__path__ = [str(dags_directory)]