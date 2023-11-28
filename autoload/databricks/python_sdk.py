
import argparse
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import compute

def execute_code(cmd, profile, cluster_id) -> str:
    client = WorkspaceClient(profile=profile)
    #cluster_id = '0420-160411-p8oi50n1'
    context = client.command_execution.create(cluster_id=cluster_id, language=compute.Language.python).result()
    response = client.command_execution.execute(cluster_id=cluster_id,
                                                context_id=context.id,
                                                language=compute.Language.python,
                                                command=cmd).result()
    client.command_execution.destroy(cluster_id=cluster_id, context_id=context.id)

    return response.results.data

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--code')
    parser.add_argument('--profile')
    parser.add_argument('--cluster_id')
    args = parser.parse_args()

    print(execute_code(args.code, args.profile, args.cluster_id))

if __name__ == "__main__":
    main()
