from itertools import count, groupby
from collections import defaultdict


class ContactIdentityNode(object):
    """ A ContactIdentityNode represents a piece of info identifying a Contact
    for e.g. for a contact like
    {"Name": "Mr. X",
    "phone": "123-456-7890",
    "email": "x@yieldmo.com"},
    we have 2 ContactIdentityNodes.
    One representing his Phone Number and the other representing his email.
    Name will not be a ContactIdentityNode because it does not uniquely identify a Contact.
    """

    def __init__(self, name):
        self._name = name
        self._connections = {}
        self._label = None

    @property
    def name(self):
        return self._name

    @property
    def connections(self):
        return self._connections

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label):
        self._label = label

    def connect_to(self, other_node):
        self._connections[other_node.name] = other_node


class ContactIdentityGraph(object):
    """
    A graph of ContactIdentityNodes.
    A raw contact is processed to establish connections between ContactIdentityNodes
    for e.g. for a contact like
    {"Name": "Mr. X",
    "phone": "123-456-7890",
    "email": "x@yieldmo.com"},
    we establish connection between ContactIdentityNode(123-456-7890) and ContactIdentityNode("x@yieldmo.com").
    Then, when we process a contact like
    {"Name": "Mr. X1",
    "phone": "123-456-7890",
    "email": "x@gmail.com"} we will establish a connection between ContactIdentityNode(123-456-7890) and
    ContactIdentityNode("x@gmail.com")
    Since these 3 nodes are connected, we now know that both the Contacts refer to the same exact person.
    We use dfs to group the ContactIdentityNodes into Connected Components
    """

    def __init__(self, name):
        self._name = name
        self._nodes = {}

    def get_node(self, node_type, name):
        full_name = node_type + ":" + name
        if not self._nodes.get(full_name):
            self._nodes[full_name] = ContactIdentityNode(full_name)
        return self._nodes[full_name]

    @staticmethod
    def connect_nodes(node_1, node_2):
        node_1.connect_to(node_2)
        node_2.connect_to(node_1)

    def label_connected_components(self):

        def label_all_nodes_starting_from(node, connected_component_label):
            """
            :param node The node that belongs to the currently traversed Connected Component
            :param connected_component_label the label for the currently traversed Connected Component
            Using DFS to find all Nodes connected to this Node
            """
            node.label = connected_component_label
            for connection in node.connections.values():
                if not connection.label:
                    label_all_nodes_starting_from(connection, connected_component_label)

        label_counter = count(start=1)
        for graph_node in self._nodes.values():
            if not graph_node.label:
                label_all_nodes_starting_from(graph_node, "Connected Component:{} ".format(next(label_counter)))


def create_graph_for_contacts(contacts_to_merge):
    """
    Processes an array of Contacts and creates a Graph. Every non empty email and phone will result in a Node in
    the graph. The nodes for a Contact will be connected.
    :param contacts_to_merge:
    :return: a ContactIdentityGraph
    """
    contact_graph = ContactIdentityGraph("Contacts Graph")
    for contact in contacts_to_merge:
        phone, email = contact.get("phone"), contact.get("email")
        # ignore empty phone
        phone_node = contact_graph.get_node("phone", phone) if phone else None
        # ignore empty email
        email_node = contact_graph.get_node("email", email) if email else None
        # connect phone and email only if both are not empty
        if phone and email:
            contact_graph.connect_nodes(phone_node, email_node)
    return contact_graph


def get_contact_key(contact, contacts_graph, unique_id_generator):
    """
    Finds the key that identifies the group for this contact.
    If this contact has either a name or an email, then we can retrive the Connected Component Label
    Else, we generate a unique Id
    :param contact: a raw contact having Name, email, and phone
    :param contacts_graph: a graph of connected components
    :param unique_id_generator: an Iterator that return a unique value on every invocation
    :return: a key identifying the connected component for this contact
    """
    contact_key = None
    contact_phone = contact.get("phone")
    contact_email = contact.get("email")
    # if a contact has phone as well as email, then the key derived from either phone or email will be same because
    # both their phone and email are in the same connected component
    if contact_phone:
        contact_key = contacts_graph.get_node("phone", contact_phone).label
    elif contact_email:
        contact_key = contacts_graph.get_node("email", contact_email).label
    else:
        # this contact has neither phone nor email
        # we have to generate unique key here so that he does not get clubbed with others with no phone and email
        contact_key = "Unconnected: {}".format(next(unique_id_generator))
    return contact_key


def merge_users(contacts_to_merge):
    """
    Creates a Graph where each vertex is an email or phone number
    A record with phone x and email y results in an edge between Vertex x and Vertex y
    Contacts that are connected by name or email can then be discovered with DFS
    This algorithm based on connected components has linear time complexity
    :param contacts_to_merge:
    :return: a list of lists. each subblist contains contacts that are related
    """
    contacts_graph = create_graph_for_contacts(contacts_to_merge)
    contacts_graph.label_connected_components()
    merged_user_groups = defaultdict(list)
    unique_id_generator = count()
    for contact_group_key, contact_iterator in groupby(contacts_to_merge,
                                                       lambda contact: get_contact_key(contact,
                                                                                       contacts_graph,
                                                                                       unique_id_generator)):
        merged_user_groups[contact_group_key].extend(list(contact_iterator))
    return merged_user_groups.values()


def print_merged_contacts(merged_contacts):
    for i, group in enumerate(merged_contacts):
        print ""
        print i
        for contact_item in group:
            print "   ", contact_item

if __name__ == "__main__":
    test_contacts = [
     {"Name": "Mr. X",  "phone": "123-456-7890", "email": "x@yieldmo.com"},
     {"Name": "Ms. Y",  "phone": "456-789-1234", "email": "y@yieldmo.com"},
     {"Name": "Mr. X1", "phone": "123-456-7890", "email": "x@gmail.com"},
     {"Name": "Ms. Y1", "phone": "456-789-9999", "email": "y@yieldmo.com"},
     {},
     {},
     {"Name": "Ken"},
     {"email ": "some1@some.com"},
     {"email": "some2@some.com"},
     {"Name": "Alan K", "phone": "123"},
     {"Name": "Alan Krauss", "phone": "123", "email": "k@gmail.com"},
     {"Name": "AK", "email": "k@gmail.com"}
    ]
    merged_contacts = merge_users(contacts_to_merge=test_contacts)
    print_merged_contacts(merged_contacts)


