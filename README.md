# aws-orgs-visualizer
Visualize your AWS org structure!

AWS organizations is an awesome way to set up your governance guardrails. However, the way that that structure is visualized leaves a little to be desired. It's also not easy to communicate to folks without access to the management account the organization structure, where their account fits into it, and what policies get applied by virtue of that placement.

The AWS org visualization tool inspects your AWS organizations structure and visualizes it in D3.

First, cd into `retrievedData` and run `python3 retrieve_data.py` to generate `orgs_data.json`. You'll need to have AWS credentials set that allow you to describe organizations in the management account.

You can either then deploy the website folder to an s3 bucket set up as a static website, or run a local python server (by executing `python3 -m http.server`, as an example) and navigate to something like `http://localhost:8000` to see your org visualized.