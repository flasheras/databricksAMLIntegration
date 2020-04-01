import os
from azureml.core.compute import ComputeTarget, DatabricksCompute
from azureml.exceptions import ComputeTargetException


def link_databricks_workspace():
    """Checks if a Databricks compute target is attached to AML. If it is not
    attached it attaches it."""
    databricks_compute_name = os.environ.get("AML_DATABRICKS_COMPUTE_NAME")
    databricks_workspace_name = os.environ.get("AML_WORKSPACE")
    databricks_resource_group = os.environ.get("AML_RESOURCE_GROUP")
    databricks_access_token = os.environ.get("AML_DATABRICKS_ACCESS_TOKEN")
    aml_workspace_name = os.environ.get("AML_WORKSPACE_NAME")
    try:
        # For automation use a Service Principal too.
        databricks_compute = DatabricksCompute(
            workspace=aml_workspace_name, name=databricks_compute_name)
        print('Compute target already exists')
    except ComputeTargetException:
        print('compute not found')
        print('databricks_compute_name {}'.format(databricks_compute_name))
        print('databricks_workspace_name {}'.format(databricks_workspace_name))
        # Unsecure
        # print('databricks_access_token {}'.format(databricks_access_token))

        # Create attach config
        attach_config = DatabricksCompute.attach_configuration(
                            resource_group=databricks_resource_group,
                            workspace_name=databricks_workspace_name,
                            access_token=databricks_access_token)
        databricks_compute = ComputeTarget.attach(
            databricks_workspace_name,
            databricks_compute_name,
            attach_config
        )

        databricks_compute.wait_for_completion(True)


if __name__ == '__main__':
    link_databricks_workspace()
