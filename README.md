# Nonprofit Networks

This codebase is a collection of tools to analyze and understand nonprofit organizations in the United States.

This codebase is separated into three components:

## Nonprofit Search

With huge thanks to [ProPublica](https://www.propublica.org/) for their [Nonprofit Explorer API](https://projects.propublica.org/nonprofits/api/), which provides the data for this project.

```python
from nonprofit_networks import ProPublicaClient

client = ProPublicaClient()
hfs = client.search("heritage foundation").organizations
hf_ein = hfs[0].ein
print(f"Evaluating {hfs[0].name} from {hfs[0].city}, {hfs[0].state}")
```
