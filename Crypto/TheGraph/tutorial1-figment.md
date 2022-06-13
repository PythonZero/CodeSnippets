Instructions for https://github.com/figment-networks/learn-web3-dapp

NOTE: To get it working, I had to update the docker-compose.yml 
```
services:
  graph-node:
    image: graphprotocol/graph-node  # change to latest version
 ipfs:
    image: ipfs/go-ipfs:v0.10.0  # change to latest vesion
 environment:
      ethereum: 'mainnet:https://eth-mainnet.alchemyapi.io/v2/<API-KEY-GOES-HERE>' # OPTIONAL - (or keep it as rpc)
```

### Setting up the connection to the mainnet (ethereum node)
```
cd docker
set ETHEREUM_RPC=mainnet:https://ethereum-mainnet--rpc.datahub.figment.io/apikey/API-KEY 
docker-compose up
```

### Install Graph CLI (graph node)
* Remember to add yarn & npm to path
```
yarn global add @graphprotocol/graph-cli
mkdir subgraphs
graph init --allow-simple-name --from-contract 0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB --network mainnet --index-events --node http://localhost:8020/ punks
# OPTIONAL: make the contract name punks
```

### Modifying the manifest
* the `subgraphs/punks/subgraph.yml` is auto-populated, but can be modified
```
# add startBlock
    source:
      startBlock: 13100000
# specify entities (see next section)
      entities:
        - Account
        - Punk
# Modify eventHandlers
      eventHandlers:
        - event: PunkBought(indexed uint256,uint256,indexed address,indexed address)
          handler: handlePunkBought
```

### Define the Schema
* The `subgraphs/punks/schema.graphql` entities need to have the two entities we specified above (`Account`, `Punk`)
    * `entities` **must have** an `id` (to index)
    * Show the 1:many `Account:Punk` relation in Account
```
type Account @entity {
  id: ID!
  # Defining the one to many relationship here from the "one" perspective
  # "an Account has many Punks"
  punksBought: [Punk!] @derivedFrom(field: "owner")
  numberOfPunkBought: BigInt!
}

type Punk @entity {
  id: ID!
  index: BigInt!
  # Defining the one to many relationship here from the "many" perspective
  # "a Punk has one Account"
  owner: Account!
  value: BigInt!
  date: BigInt!
}
```
* Then generate the entities' boilerplate code
  * defines typescript classes for each entity (`generated/schema.ts`)
```
cd punks
yarn codegen
```

### Map events to entities
1. Run `yarn add @graphprotocol/graph-ts`
2. In `subgraphs/punks/src/contract.ts`
    ```js
    // solution
    import {BigInt} from '@graphprotocol/graph-ts';
    
    import {PunkBought as PunkBoughtEvent} from '../generated/Contract/Contract';
    import {Account, Punk} from '../generated/schema';
    
    export function handlePunkBought(event: PunkBoughtEvent): void {
      let account = Account.load(event.params.toAddress.toHexString());
    
      if (account == null) {
        account = new Account(event.params.toAddress.toHexString());
        account.id = event.params.toAddress.toHexString();
        account.numberOfPunkBought = BigInt.fromI32(1);
      } else {
        account.numberOfPunkBought = account.numberOfPunkBought.plus(
          BigInt.fromI32(1),
        );
      }
    
      account.save();
    
      let punk = Punk.load(event.params.punkIndex.toHexString());
    
      if (punk == null) {
        punk = new Punk(event.params.punkIndex.toHexString());
        punk.id = event.params.punkIndex.toHexString();
        punk.index = event.params.punkIndex;
      }
    
      punk.owner = event.params.toAddress.toHexString();
      punk.value = event.params.value;
      punk.date = event.block.timestamp;
    
      punk.save();
    }
    ```
3. In `subgraphs\punks`:
   1. `yarn create-local`
   2. `yarn deploy-local`  # this now hosts your graphql webserver

4. Access your `deploy-local` from `http://localhost:8000/subgraphs/name/punks`

