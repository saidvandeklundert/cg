from builder import (
    NetworkBuilder,
    load_communities,
    load_secrets_from_vault,
    load_information_from_ssot,
)

if __name__ == "__main__":

    community_input = load_communities()
    secrets_input = load_secrets_from_vault()
    network_input = load_information_from_ssot()
    network = NetworkBuilder(
        network=network_input, communities=community_input, secrets=secrets_input
    )
