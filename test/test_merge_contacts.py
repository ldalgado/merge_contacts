from pytest import *
from merge_contacts import ContactIdentityNode, ContactIdentityGraph, merge_users, print_merged_contacts


def test_contact_identity_node_name():
    node = ContactIdentityNode("Some Name")
    assert node.name == "Some Name", "ContactIdentityNode name is not set"


def test_contact_identity_node_label():
    node = ContactIdentityNode("Some Name")
    node.label = "Some Label"
    assert node.label == "Some Label", "ContactIdentityNode label is not set"


def test_contact_identity_node_connections():
    node1 = ContactIdentityNode("Node1")
    node2 = ContactIdentityNode("Node2")
    node3 = ContactIdentityNode("Node3")
    node1.connect_to(node2)
    node1.connect_to(node3)
    assert node1.connections == {node2.name: node2, node3.name: node3}, "ContactIdentityNode connections are not set"


def test_contact_identity_graph_connected_components():
    graph = ContactIdentityGraph("ContactIdentityGraph")
    node1 = graph.get_node("phone", "phone1")
    node2 = graph.get_node("phone", "phone2")
    node3 = graph.get_node("phone", "phone3")
    graph.connect_nodes(node1, node2)
    graph.label_connected_components()
    assert node1.label == node2.label, "ContactIdentityGraph could not calculate Connected Comps"
    assert node3.label != node1.label, "ContactIdentityGraph could not calculate Connected Comps"


def test_contact_identity_graph_connected_components():
    graph = ContactIdentityGraph("ContactIdentityGraph")
    node1 = graph.get_node("phone", "phone1")
    node2 = graph.get_node("phone", "phone2")
    node3 = graph.get_node("phone", "phone3")
    graph.connect_nodes(node1, node2)
    graph.label_connected_components()
    assert node1.label == node2.label, "ContactIdentityGraph could not calculate Connected Comps"
    assert node3.label != node1.label, "ContactIdentityGraph could not calculate Connected Comps"


def create_contact(**kwargs):
    return kwargs


def test_merge_users_with_duplicates():
    user1 = create_contact(Name="user1", email="email1", phone="phone1")
    duplicate_user1 = create_contact(Name="user1", email="email1", phone="phone1")
    merged_groups = merge_users([user1, duplicate_user1])
    assert len(merged_groups) == 1, "Duplicate contacts are not merged!"
    assert user1 in merged_groups[0], "Duplicate contacts are not merged correctly!"


def test_merge_users_with_two_sets_of_duplicates():
    user1 = create_contact(Name="user1", email="email1", phone="phone1")
    duplicate_user1 = create_contact(Name="user1", email="email1", phone="phone1")

    user2 = create_contact(name="user2", email="email2", phone="phone2")
    duplicate_user2 = create_contact(name="user2", email="email2", phone="phone2")

    merged_groups = merge_users([user1, duplicate_user1, user2, duplicate_user2])
    assert len(merged_groups) == 2, "Duplicate contacts are not merged!"


def test_merge_users_with_different_phone_or_email():
    user1 = create_contact(Name="user1", email="email1", phone="phone1")
    user1_different_email = create_contact(Name="user1", email="email1-different", phone="phone1")
    user1_different_phone = create_contact(Name="user1", email="email1", phone="phone1-different")

    user2 = create_contact(Name="user2", email="email2", phone="phone2")
    user2_different_phone = create_contact(name="user2", email="email2", phone="phone2-different")

    merged_groups = merge_users([user1, user1_different_email, user1_different_phone, user2, user2_different_phone])
    assert len(merged_groups) == 2, "Users with varying phone or emal are not merged!"
    
    user1_group = filter(lambda group: group[0]["Name"] == "user1",  merged_groups)[0]
    assert len(user1_group) == 3, "Users varying by email are not grouped correctly"
    assert user1 in user1_group, "Users varying by email are not grouped correctly"
    assert user1_different_email in user1_group, "Users varying by email are not grouped correctly"
    assert user1_different_phone in user1_group, "Users varying by phone are not grouped correctly"

    user2_group = filter(lambda group: group[0]["Name"] == "user2",  merged_groups)[0]
    assert user2 in user2_group, "Users varying by phone are not grouped correctly"
    assert user2_different_phone in user2_group, "Users varying by phone are not grouped correctly"


def test_merge_users_with_no_phone_or_email():
    user1_no_phone_email = create_contact(Name="user1")
    user2_no_phone_email = create_contact(Name="user2")

    merged_groups = merge_users([user1_no_phone_email, user2_no_phone_email])
    print_merged_contacts(merged_groups)
    assert len(merged_groups) == 2, "Users with no phone or email are not handled!"

    user1_group = filter(lambda group: group[0]["Name"] == "user1",  merged_groups)[0]
    assert len(user1_group) == 1, "User with no phone or email are not handled"
    assert user1_no_phone_email in user1_group , "User with no phone or email are not handled"

    user2_group = filter(lambda group: group[0]["Name"] == "user2",  merged_groups)[0]
    assert len(user2_group) == 1, "User with no phone or email are not handled"
    assert user2_no_phone_email in user2_group , "User with no phone or email are not handled"
