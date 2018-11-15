from kubernetes import client
import json

def lambda_handler(event, context):
    # TODO implement
    ret = eks()
    return {
    "sessionAttributes": {
    "key1": "value1",
    "key2": "value2"
  },
  "dialogAction": {
    "type": "Close",
    "fulfillmentState": "Fulfilled",
    "message": {
      "contentType": "PlainText",
      "content": str (ret)
    }
  }
}

def eks():
    ApiToken = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tcDk2czciLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjAyZmIwMDJhLWU3ZmQtMTFlOC05YjJlLTAyYzQyMmQ0OWJmZSIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.ibia1N3GOM7csXhLOBiii2VJACyE0gd17dfQErZdmegq4x3nPgqcLdvxW5MKNhcmX5K6M_JyeXDLXPAljdB0MY6Z2sfZ0hyIszEJ7w9MGszZvAutKa3HGZ9M16iNksud1sNl0lz3lDLp8v4OEumbjIicJwD5SBV_FUID9cfP6yMEXR0kVdsAJ2Wtw9ua861xH5K1AE8SiQy2ui-Gb-0iD02IVyrwBT2JigYIdheiDg8uFNJrOdlRVPlwytW2S8cZxPVLDKesbtYmTqoLrysMzx0VrvW8rvWOlwaFgc99lyHvOesMJu92ZWd6BRaGDJn7rgiOoAh0Vr5V_DIQjmjIaA'
    configuration = client.Configuration()
    configuration.host = 'https://C265CA934A4A7DE2C7FA650C8481BABD.sk1.eu-west-1.eks.amazonaws.com'
    configuration.verify_ssl = False
    configuration.debug = True
    configuration.api_key['authorization'] = "Bearer " + ApiToken
    configuration.assert_hostname = True
    client.Configuration.set_default(configuration)

    v1 = client.CoreV1Api()
    ret = v1.list_pod_for_all_namespaces(watch=False)
    print(ret)
    return ret


