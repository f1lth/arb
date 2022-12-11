import { ethers } from 'ethers'
import IUniswapV2Pair from './abi/IUniswapV2Pair.json'

const provider = new ethers.providers.JsonRpcProvider('https://polygon-mainnet.g.alchemy.com/v2/CgqAh4Ifjhpq7TBIzigvS1-x9gqfAqCI')

async function main() {
  // get the latest block from the polygon mainnet
  const block = await provider.getBlockNumber()
  console.log(block)

  const UNI_FACTORY_ADDY = '0x1F98431c8aD98523631AE4a59f267346ea31F984'

  const first_pair = {
        "index": 0, 
        "address": "0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc", 
        "token0": { 
            "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", 
            "symbol": "USDC", 
            "decimal": 6
          }, 
          "token1": {
              "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2", 
              "symbol": "WETH", 
              "decimal": 18
            }, 
            "reserve0": 176560092727090, 
            "reserve1": 524595304157729979983018}
}




/**
 * def generate_get_reserves_json_rpc(pairs, blockNumber='latest'):
    c = w3.eth.contract(abi=pairABI) 
    for pair in pairs:
        yield generate_json_rpc(
                method='eth_call',
                params=[{
                    'to': pair['address'],
                    'data': c.encodeABI(fn_name='getReserves', args=[]),
                    },
                    hex(blockNumber) if blockNumber != 'latest' else 'latest',
                    ]
                )
 */

main()

