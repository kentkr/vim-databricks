
import argparse
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import compute

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--code')
    args = parser.parse_args()

    client = WorkspaceClient()
    cluster_id = ''
    context = client.command_execution.create(cluster_id=cluster_id, language=compute.Language.PYTHON).result()
    results = client.command_execution.create(cluster_id=cluster_id,
                                              context_id=context.id,
                                              language=compute.Language.PYTHON,
                                              command = args.code)
    client.command_execution.destroy(cluster_id=cluster_id, context_id=context.id)
    print(args.code)

if __name__ == "__main__":
    main()
