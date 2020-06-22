# Azure Log Analytics Examples

## Scripts
1. [Powershell Example](/src/powershell_example/log_deployment_details.ps1)
   - Logs deployment times and other pipeline parameters from the release pipeline to Azure Monitor (Log analytics workspace)
2. [Python Example](/src/python_example/push_ado_logs.py)
   - python3 example
   - Logs the deployment logs to Azure Monitor

## Usage
1. Create a release pipeline
2. Add an agent task (either Powershell script or Python Script)
3. Use the "script path" option or "inline" option and point to the above scripts
4. Add values to the environment variables (as pipeline variables or env variables) used in the script
5. Optionally save the task in the Task Group and reuse in other stages or pipelines
6. Run the pipeline
7. NOTE: It can take upto 5 minutes for the logs to appear in Azure Log Analytics Workspace
