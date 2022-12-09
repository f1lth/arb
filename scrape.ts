import { ethers } from 'ethers'

const provider = new ethers.providers.JsonRpcProvider('https://polygon-mainnet.g.alchemy.com/v2/CgqAh4Ifjhpq7TBIzigvS1-x9gqfAqCI')

async function main() {
  // get the latest block from the polygon mainnet
  const block = await provider.getBlockNumber()
  console.log(block)

}

main()

