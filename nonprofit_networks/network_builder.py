import abc
import datetime
import networkx as nx

from nonprofit_networks.response_types import Form990PartVIISectionAGrp_
from .propublica_sdk import ProPublicaClient

Ein = str

THIS_YEAR = datetime.datetime.now().year


class NetworkBuilder(abc.ABC):
    def get_graph(self): ...


class NetworkXNetworkBuilder(NetworkBuilder):
    graph: nx.MultiDiGraph

    def get_graph(self):
        return self.graph


class GrantmakerNetworkBuilder(NetworkXNetworkBuilder):
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
            ein, filing=filing, name=filing.get_name(), __labels__=set(["Organization"])
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
                        __labels__=set(["Organization"]),
                    )
                except Exception:
                    continue
            self.graph.add_edge(
                ein,
                grant.RecipientEIN,
                grant=grant,
                amount=grant.CashGrantAmt,
                memo=grant.PurposeOfGrantTxt,
                __labels__=set(["GrantFunded"]),
            )
            self._build_network(grant.RecipientEIN, depth - 1, year)


class StaffNetworkBuilder(NetworkXNetworkBuilder):
    def __init__(
        self,
        client: ProPublicaClient,
        existing_graph: nx.MultiDiGraph | None = None,
        organization_subset: list[Ein] | None = None,
    ):
        self.client = client
        self.graph = existing_graph or nx.MultiDiGraph()
        self.organization_subset = organization_subset or []

    def build_network(self):
        # For every org in the network (or the subset if provided),
        # get the staff and add them to the graph
        if not self.organization_subset:
            self.organization_subset = [
                ein
                for ein in self.graph.nodes()
                if "Organization" in self.graph.nodes[ein].get("__labels__")
            ]

        # The vertices will have a `filing` attribute that contains the full filing
        for ein_node_id in self.organization_subset:
            filing = self.graph.nodes[ein_node_id]["filing"]
            staff: list[Form990PartVIISectionAGrp_] = filing.get_staff()
            for staff_member in staff:
                name = staff_member.PersonNm
                if not name:
                    continue

                # Add the staff member to the graph
                self.graph.add_node(
                    staff_member.PersonNm,
                    filing=filing,
                    name=filing.get_name(),
                    __labels__=set(["Person"]),
                )
                # Add an edge from the organization to the staff member
                self.graph.add_edge(
                    ein_node_id,
                    staff_member.PersonNm,
                    __labels__=set(["StaffMember"]),
                )

                # Search the staff member and see if they have other organizations
                # self.client.search_people(name, nonprofit_ein=ein_node_id)
                search_results = self.client.search_people(name)
                for result in search_results:
                    # Check if the result is legit. state is the same prob
                    # and also each word in the name.lower() is also in the
                    # result name
                    search_names = result.name.lower().split()
                    # if result.state != filing.get_state():
                    #     continue
                    if not all(word in result.name.lower() for word in search_names):
                        print(f"FAIL {result.name} --- {name}")
                        continue
                    # Add the result to the graph
                    # Check if the result is already in the graph
                    if result.nonprofit_ein in self.graph:
                        continue
                    self.graph.add_node(
                        result.nonprofit_ein,
                        name=result.nonprofit,
                        __labels__=set(["Organization"]),
                    )
                    # Add an edge from the staff member to the result
                    self.graph.add_edge(
                        staff_member.PersonNm,
                        result.nonprofit_ein,
                        __labels__=set(["StaffMember"]),
                    )
