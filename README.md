# Nonprofit Networks

This codebase is a collection of tools to analyze and understand nonprofit organizations in the United States.

[![Run on colab](https://img.shields.io/badge/Run_on-Colab-Red?style=for-the-badge&logo=google)](https://colab.research.google.com/github/j6k4m8/nonprofit_networks/blob/main/docs/Example-Grassroots.ipynb) [![Static Badge](https://img.shields.io/badge/No_nazis_allowed-yay-green?style=for-the-badge)](https://github.com/j6k4m8/nonprofit_networks/blob/main/LICENSE#L9)

This codebase is separated into three components:

## Nonprofit Search

With huge thanks to [ProPublica](https://www.propublica.org/) for their [Nonprofit Explorer API](https://projects.propublica.org/nonprofits/api/), which provides the data for this project.

```python
from nonprofit_networks import ProPublicaClient

client = ProPublicaClient()
org = client.search("donors trust", state="VA", city="Alexandria").organizations[0]]
```

## Nonprofit Filing Details

```python
filing = client.get_full_filing(org.ein, 2024)

for comp in filing.get_compensations():
    print(
        f"{comp.PersonNm:<30} {comp.TitleTxt:<30} ${comp.ReportableCompFromOrgAmt:>10,.2f} (plus ${comp.OtherCompensationAmt:>10,.2f})"
    )
```

```
Kimberly O Dennis              Chair                          $      0.00 (plus $      0.00)
James Piereson                 Vice Chair                     $      0.00 (plus $      0.00)
Thomas E Beach                 Director                       $      0.00 (plus $      0.00)
George GH Coates Jr            Director                       $      0.00 (plus $      0.00)
Lawson R Bader                 President and CEO              $393,490.00 (plus $ 72,461.00)
Jeffrey C Zysik                CFO, COO and Treasurer         $305,587.00 (plus $ 60,430.00)
Peter A Lipsett                Vice President / Secretary     $227,897.00 (plus $ 54,136.00)
Stephen M Johnson              CTO                            $181,250.00 (plus $ 39,742.00)
Gregory P Conko                Vice President of Programs     $225,392.00 (plus $ 46,106.00)
Lukas C Dwelly                 Philanthropic Advisor          $179,667.00 (plus $ 40,346.00)
Stephanie L Giovanetti         Philanthropic Advisor          $156,175.00 (plus $ 23,164.00)
Christopher D Renner           Controller                     $161,704.00 (plus $ 41,228.00)
Elia J Peterson                Assistant Controller           $115,569.00 (plus $ 25,044.00)
```

```python
filing.get_net_assets()
```

> **$1,289,047,383.00**

See also,

| Method                          | Description                                            |
| ------------------------------- | ------------------------------------------------------ |
| `get_compensations`             | Get a list of all reported compensation to staff/board |
| `get_contractor_compensation`   | Get a list of all reported compensation to contractors |
| `get_grant_recipients`          | Get a list of all grant recipients (including EINs)    |
| `get_total_revexp`              | Get the total revenue and expenses                     |
| `get_net_assets`                | Get the net assets                                     |
| `get_rent_income`               | Get a list of rent income                              |
| `get_disregarded_entities`      | Get a list of disregarded entities                     |
| `get_related_tax_exempt_orgs`   | Get a list of related tax exempt orgs                  |
| `get_transactions_related_orgs` | Get a list of transactions with related orgs           |

## Network Traversal

### Grantmakers

This tool makes it easy to traverse the network of grantmaking organizations:

```python
from nonprofit_networks import ProPublicaClient
from nonprofit_networks.network_builder import GrantmakerNetworkBuilder

client = ProPublicaClient()
org = client.search(...).organizations[0]

grant_net = GrantmakerNetworkBuilder(client)
grant_net.build_network(org.ein, depth=2, year=2023)
```

These networks have vertices of organizations, and the edges have an `amount` attribute that represents the amount of the grant.

```python
longest_path = nx.dag_longest_path(grant_net.graph)
    print("Longest path:")
    for i in range(len(longest_path) - 1):
        node = longest_path[i]
        next_node = longest_path[i + 1]
        amount = grant_net.graph[node][next_node][0]["grant"].CashGrantAmt
        print(
            # f"{grant_net.graph.nodes[node]['filing'].get_name()} "
            f"${amount:,.2f} -> "
            f"{grant_net.graph.nodes[next_node]['filing'].get_name()}"
        )
```

```
Longest Path:

Donor's Trust →
    $12,727,215.00 → BRADLEY IMPACT FUND INC
    $35,000.00 → STATE POLICY NETWORK
    $125,000.00 → Center of the American Experiment
    $109,000.00 → JUDICIAL WATCH INC
    $5,000.00 → COALITIONS FOR AMERICA
```

(Note that in this example it is clear that the `amount` does not all come from the same parent organization or from the same grant, since of course later edges can have larger dollar amounts than earlier edges. While this is useful for "tracing the money", it is not useful for understanding the flow of individual grant allocations.)

You can render these graphs with, for example,

```python
import networkx as nx
import matplotlib.pyplot as plt

sanitized_graph = grant_net.graph.copy()
# Remove anything with net_assets == None, and print them
for node in list(sanitized_graph.nodes):
    if sanitized_graph.nodes[node]['filing'].get_net_assets() is None:
        print(f"Removing {sanitized_graph.nodes[node]['filing'].get_name()}")
        sanitized_graph.remove_node(node)

node_sizes = [(sanitized_graph.nodes[node]['filing'].get_net_assets())/100000 for node in sanitized_graph.nodes]
node_colors = [(sanitized_graph.nodes[node]['filing'].get_total_revexp()[0])/100000 for node in sanitized_graph.nodes]

plt.figure(figsize=(16, 16), dpi=100)
pos = nx.spring_layout(sanitized_graph, weight="amount")
nx.draw_networkx_labels(sanitized_graph, pos, labels={node: sanitized_graph.nodes[node]['filing'].get_name() + "\n\n" for node in sanitized_graph.nodes}, font_size=8)
edges = nx.draw_networkx_edges(sanitized_graph, pos, edge_color='gray', alpha=0.5, node_size=node_sizes, width=[sanitized_graph.edges[edge]['amount']**0.1 for edge in sanitized_graph.edges])
nx.draw_networkx_nodes(sanitized_graph, node_size=node_sizes, node_color=node_colors, cmap='viridis', pos=pos)
plt.show()
```
