
import argparse
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import compute

def execute_code(cmd: str, profile: str, cluster_id: str) -> str:
    """
    Send python code to execute on databricks. It currenly creates a new execution
    context for each run. 

    Parameters:
        cmd (str): Python code to execute
        profile: Databricks profile set up in ~/.databrickscfg
        cluster_id: the cluster id for code to be executed on

    Returns:
        str: command output
    """
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
    """
    When script is ran read in args and execute code
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--code')
    parser.add_argument('--profile')
    parser.add_argument('--cluster_id')
    args = parser.parse_args()

    print(execute_code(args.code, args.profile, args.cluster_id))

if __name__ == "__main__":
    main()
