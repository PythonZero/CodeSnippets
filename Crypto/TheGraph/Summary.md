# The Graph

- Allows querying & indexing smart contracts on the blockchain

- ```
  DAPP    ---txn--->     CONTRACT    ---event---> ETH
   |          1                           2        ↑
   |                                               | scans new block
   |                                               |        |
   |------------------→ GRAPH NODE  ---------------|        |
   query w/ graphql         ↑              3                | 4
                            |                               |
                            |                               ↓
                            |________________________ ENTITY MAPPER
                                    indexed           (WASM Module)
  ```

## Important Notes
* Setting up a **graph node** (like a local webserver -> dev -> publish)
  * Have many subgraphs (i.e. at least one per contract)
* **Graph Node** = **IPFS Swarm** (stores subgraph) + **PostgreSQL** (stores processed events) + **GraphQL** (queries db)
* **IPFS** = InterPlanetary FileSystem. A distributed filesystem to store/access info

## Graph Node Setup Summary
 
 1. Use an [**ethereum node** provider](https://ethereum.org/en/developers/docs/nodes-and-clients/nodes-as-a-service/#popular-node-services) (i.e. alchemy)
 2. Run your **graph node** locally via the graph-cli (docker-compose up)
 3. Create a subgraph for your smart contract (cryptopunks)
    * `graph init` (by `yarn global add @graphprotocol/graph-cli`)
    * Creates the manifest (`.yaml`), ABI, schema (`.graphql`) , mappings (`.ts`)
4. Modify the manifest `subgraph.yaml`
    * i.e. specify startBlock/entities/eventHandlers
5. Modify the `schema.graphql`
    * specifies entities and relations (1:1, 1:many)
6. Compile the `.graphql` -> `.ts`
   * `cd punks; yarn codegen`
7. Map **events** to **entities* `src/mapping.ts`
8. Deploy the subgraph
   * `yarn create-local`
   * `yarn deploy-local` -> http://localhost:8000/subgraphs/name/punks
9. Query the graphql from      ↑

## Users
1. **Curators** - subgraph developers decide what to index
2. **Indexers** - node operators -> offer indexing + querying (i.e. what we have setup above)
3. **Delegators** - delegate GRT tokens to indexers -> don't need a full node to query
