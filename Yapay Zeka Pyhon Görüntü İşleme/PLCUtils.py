from opcua import Client, ua

def read_input_value(client, node_id):
    client_node = client.get_node(node_id)  # get node
    client_node_value = client_node.get_value()  # read node value
    print("Value of : " + str(client_node) + ' : ' + str(client_node_value))


def write_value_int(client, node_id, value):
    client_node = client.get_node(node_id)  # get node
    client_node_value = value
    client_node_dv = ua.DataValue(ua.Variant(client_node_value, ua.VariantType.Int16))
    client_node.set_value(client_node_dv)
    print("Value of : " + str(client_node) + ' : ' + str(client_node_value))


def write_value_bool(client, node_id, value):
    client_node = client.get_node(node_id)  # get node
    client_node_value = value
    client_node_dv = ua.DataValue(ua.Variant(client_node_value, ua.VariantType.Boolean))
    client_node.set_value(client_node_dv)
    print("Value of : " + str(client_node) + ' : ' + str(client_node_value))


def client_connection(url):
    try:
        client = Client(url)
        client.connect()
        print("Connected to OPC UA Server with url :", url)
    except:
        client = None
        print("Unable to connect to OPC UA Server with url :", url)
    return None