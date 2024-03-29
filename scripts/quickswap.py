from web3 import Web3
from eth_abi import decode_abi
from web3._utils.request import make_post_request
from web3 import HTTPProvider
import json
import numpy as np
from dotenv import load_dotenv

'''
                        $$\                 $$\    
                        \__|                $$ |   
 $$$$$$\  $$$$$$\$$$$\  $$\ $$$$$$$\   $$$$$$$ |   
$$  __$$\ $$  _$$  _$$\ $$ |$$  __$$\ $$  __$$ |   
$$ /  $$ |$$ / $$ / $$ |$$ |$$ |  $$ |$$ /  $$ |   
$$ |  $$ |$$ | $$ | $$ |$$ |$$ |  $$ |$$ |  $$ |   
\$$$$$$$ |$$ | $$ | $$ |$$ |$$ |  $$ |\$$$$$$$ |   
 \____$$ |\__| \__| \__|\__|\__|  \__| \_______|   
      $$ |                                         
      $$ |         2022  -  2023  season                               
      \__|         DISRUPTIVE TECHNOLOGY 
                   FILE: quickswap.py
                   PURPOSE: methods to pull data from quickswap exchange
'''

pairABI = json.load(open('../abi/IUniswapV2Pair.json'))['abi']
qsPairABI = json.load(open('../abi/IUniswapQSPair.json'))['abi']
erc20ABI = json.load(open('../abi/ERC20.json'))['abi']
pairs = json.load(open('../files/pairs.json'))

MAINNET_RPC = PROCESS.ENV.MAINNET_RPC
POLYGON_RPC = PROCESS.ENV.POLYGON_RPC
QUICKSWAP_CONTRACT = '0x5757371414417b8C6CAad45bAeF941aBc7d3Ab32'

w3 = Web3(Web3.HTTPProvider(POLYGON_RPC))
qs = w3.eth.contract(abi=qsPairABI)

# Batch http request provider
class BatchHTTPProvider(HTTPProvider):

    def make_batch_request(self, text):
        self.logger.debug("Making request HTTP. URI: %s, Request: %s",
                          self.endpoint_uri, text)
        request_data = text.encode('utf-8')
        raw_response = make_post_request(
            self.endpoint_uri,
            request_data,
            **self.get_request_kwargs()
        )
        response = self.decode_rpc_response(raw_response)
        self.logger.debug("Getting response HTTP. URI: %s, "
                          "Request: %s, Response: %s",
                          self.endpoint_uri, text, response)
        return response

#  generates the json format we need to make a batch request
def generate_json_rpc(method, params, request_id=1):
    return {
        'jsonrpc': '2.0',
        'method': method,
        'params': params,
        'id': request_id,
    }

# generates the json format for the pairs
def generate_get_reserves_json_rpc(pairs, blockNumber='latest'):
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


# format the http request and pull the data out of it
def gen_polygon_pairs(save=False):
    
    pairs = list()
    tokens = set()
    # read from the quickswap contract on the polygon chain
    qswap_contract = w3.eth.contract(abi=qsPairABI, address=QUICKSWAP_CONTRACT)
    
    TOTAL_LENGTH = qswap_contract.functions.allPairsLength().call()
    TEST_LENGTH = 100

    for i in range(TEST_LENGTH):
        if i % 10 == 0:
            print(f'generating...({i} / {TOTAL_LENGTH})')
        # get the address of the pair 
        pool_i = qswap_contract.functions.allPairs(i).call()
        # get the token0 and token1 addresses using 
        # IUserUniswapV2Pair interface and the pool's addy
        univ2pair = w3.eth.contract(abi=pairABI, address=pool_i)
        address0 = univ2pair.functions.token0().call()
        address1 = univ2pair.functions.token1().call()
        # format the data to jsonify!
        token0contract = w3.eth.contract(abi=erc20ABI, address=address0)
        token0 = {'token0': {
            'address': address0,
            'symbol': token0contract.functions.symbol().call(),
            'decimal': token0contract.functions.decimals().call()
        }}
        token1contract = w3.eth.contract(abi=erc20ABI, address=address1)
        token1 = {'token1': {
            'address': address1,
            'symbol': token1contract.functions.symbol().call(),
            'decimal': token0contract.functions.decimals().call(),
        }}
        # add the addresses to the set if they're not in there already
        if address0 not in tokens:
            tokens.add(address0)
        if address1 not in tokens:
            tokens.add(address1)

        out = {
            'index': i,
            'address': pool_i,
            'token0': token0,
            'token1': token1

        }
        #[{ "index": 0, 
        #   "address": "0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc",              # pool i 
        #   "token0": {
        #       "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",          # address0
        #       "symbol": "USDC", 
        #       "decimal": 6
        #       }, 
        #   "token1": {
        #       "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",          # address0
        #       "symbol": "WETH", 
        #       "decimal": 18
        #       }, 
        #   "reserve0": 176560092727090, 
        #   "reserve1": 524595304157729979983018
        # }]
        pairs.append(out)
    # dont need to do this often, just sometimes, not that often tho
    if save:
        with open('../files/polygon_pairs.json', 'w') as f:
            json.dump(pairs, f)

    return pairs, tokens

# format the http request and pull the data out of it
def get_reserve_json(pairs, blockNumber='latest'):
    # loop through the list of pairs
    for pair in pairs:
        c = w3.eth.contract(abi=pairABI, address=pair['address'])
        yield generate_json_rpc(
                method='eth_call',
                params=[{
                    'to': pair['address'],
                    'data': c.encodeABI(fn_name='getReserves', args=[]),
                    },
                    blockNumber,
                    ]
                )
        
# pull the result for each response
def rpc_response_to_result(response):
    result = response.get('result')
    if result is None:
        error_message = 'result is None in response {}.'.format(response)
        if response.get('error') is None:
            error_message = error_message + ' Make sure Ethereum node is synced.'
            # When nodes are behind a load balancer it makes sense to retry the request in hopes it will go to other synced node.
            raise RuntimeError(error_message)
        raise ValueError(error_message)
    return result

def rpc_response_batch_to_results(response):
    for response_item in response:
        yield rpc_response_to_result(response_item)

def get_reserves(pairs):
    # make a batch of http requests from the list of pairs
    batch_provider = BatchHTTPProvider(endpoint_uri=POLYGON_RPC)
    calldata = list(get_reserve_json(pairs))
    resp = batch_provider.make_batch_request(json.dumps(calldata))
    results = list(rpc_response_batch_to_results(resp))

    reserves = list()
    for i in range(len(pairs)):
        res = decode_abi(['uint256', 'uint256', 'uint256'], bytes.fromhex(results[i][2:]))
        reserves.append((res[0], res[1]))

    return reserves

# accepts a json list of pairs and returns 
# them in dictionary form
def toDict(pairs):
    p = {}
    i = 0
    for pair in pairs:
        p[pair['address']] = pair
        p[pair['address']]['arrIndex'] = i
        i += 1
    return p

