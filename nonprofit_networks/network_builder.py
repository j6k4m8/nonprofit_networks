import abc
import datetime
import networkx as nx
from .propublica_sdk import ProPublicaClient

Ein = str

THIS_YEAR = datetime.datetime.now().year


class NetworkBuilder(abc.ABC):
    def get_graph(self): ...


class GrantmakerNetworkBuilder(NetworkBuilder):

    def __init__(
        self, client: ProPublicaClient, existing_graph: nx.MultiDiGraph | None = None
    ):
        self.client = client
        self.graph = existing_graph or nx.MultiDiGraph()

    def build_network(self, ein: Ein, depth: int, year: int = THIS_YEAR - 1):
        self._build_network(ein, depth, year)

    def _build_network(self, ein: Ein, depth: int, year: int = THIS_YEAR - 1):
        if depth == 0:
            return
        filing = self.client.get_full_filing(ein, year)
        self.graph.add_node(
            ein, filing=filing, name=filing.get_name(), __labels__=set("Organization")
        )
        for grant in filing.get_grant_recipients():
            if not grant.RecipientEIN or not isinstance(grant.RecipientEIN, str):
                continue
            if grant.RecipientEIN not in self.graph:
                try:
                    filing = self.client.get_full_filing(grant.RecipientEIN, year)
                    self.graph.add_node(
                        grant.RecipientEIN,
                        filing=filing,
                        name=filing.get_name(),
                        __labels__=set("Organization"),
                    )
                except Exception:
                    continue
            self.graph.add_edge(
                ein,
                grant.RecipientEIN,
                grant=grant,
                amount=grant.CashGrantAmt,
                memo=grant.PurposeOfGrantTxt,
                __labels__=set("GrantFunded"),
            )
            self._build_network(grant.RecipientEIN, depth - 1, year)
