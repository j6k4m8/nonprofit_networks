# Nonprofit Networks

This codebase is a collection of tools to analyze and understand nonprofit organizations in the United States.

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

[Coming soon]
