from model import Communities, Network
from typing import Dict
from jinja2 import Environment, FileSystemLoader
import yaml


def load_communities() -> Communities:
    """Mocking data retrieval from 'something'."""
    with open("communities.yaml") as f:
        data = yaml.safe_load(f)

    communities = Communities(**data)

    return communities


def load_secrets_from_vault() -> Dict[str, str]:
    """Retrieves secrets information from Vault"""

    with open("secrets.yaml") as f:
        secrets_data = yaml.safe_load(f)

    return secrets_data


def load_information_from_ssot() -> Network:
    """Retreives information from SSOT"""

    with open("devices.yaml") as f:
        data = yaml.safe_load(f)
    network = Network(**data)
    return network


class NetworkBuilder:
    """Class that builds the data schema and the network configuration"""

    def __init__(self, network: Network, communities: Communities, secrets: dict):
        self.network = network
        self.communities = communities
        self.secrets = secrets
        self.build_network()
        self.store_schema()
        self.render_templates()

    def build_network(self):
        """Implements additional build logic

        In this example, only community data is added to the network device.

        """
        for device in self.network.devices:
            if device.role == "leaf":
                device.communities = self.communities
            device.secrets = self.secrets

        return self.network

    def store_schema(self):
        """Store the 'per device' schema."""
        for device in self.network.devices:
            with open(f"{device.name}.json", "w") as f:
                f.write(device.json(indent=2))

    def render_templates(self):
        """Render the templates and write the configuration to disk."""
        for device in self.network.devices:
            device_name = device.name
            file_loader = FileSystemLoader("templates")
            env = Environment(loader=file_loader)

            template = env.get_template("template.j2")
            output = template.render(data=device.dict())
            if output:
                # avoid the Jinja whitespace nonesense:
                output = "\n".join(
                    [line for line in output.splitlines() if line.strip()]
                )
                with open(f"{device_name}.cfg", "w") as f:
                    f.write(output)
                print(f"\n\nRendered {device_name}.cfg\n\n")
                print(output)
            else:
                raise RuntimeError("No template output!!")
