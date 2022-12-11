from uniswap import Uniswap
from web3 import Web3
from eth_abi import decode_abi
from web3._utils.request import make_post_request
from web3 import HTTPProvider
import json

pairABI = json.load(open('../abi/IUniswapV2Pair.json'))['abi']
qsPairABI = json.load(open('../abi/IUniswapQSPair.json'))['abi']
pairs = json.load(open('../files/pairs.json'))

MAINNET_RPC = 'https://eth-mainnet.g.alchemy.com/v2/_6fKb6sxb6cRqisT68ysJiX759z1J0a-'
POLYGON_RPC = "https://polygon-mainnet.g.alchemy.com/v2/CgqAh4Ifjhpq7TBIzigvS1-x9gqfAqCI"
w3 = Web3(Web3.HTTPProvider(POLYGON_RPC))

qs_addy = '0x5757371414417b8C6CAad45bAeF941aBc7d3Ab32'
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
def generate_polygon_pairs( blockNumber='latest'):
    # get latest polygon block number
    blockNumber = hex(w3.eth.blockNumber)
    d = w3.eth.contract(abi=qsPairABI) 

    return generate_json_rpc(
            method='eth_call',
            params=[{
                'to': qs_addy,
                'data': d.encodeABI(fn_name='allPairsLength', args=[]),
                },
                blockNumber ,
                ]
            )

# pull the result for each response
def rpc_response_to_result(response):
    result = response.get('result')
    if result is None:
        error_message = 'result is None in response {}.'.format(response)
        if response.get('error') is None:
            error_message = error_message + ' Make sure Ethereum node is synced.'
            # When nodes are behind a load balancer it makes sense to retry the request in hopes it will go to other,
            # synced node
            raise RuntimeError(error_message)

        raise ValueError(error_message)
    return result

def rpc_response_batch_to_results(response):
    for response_item in response:
        yield rpc_response_to_result(response_item)

#r = list(generate_get_reserves_json_rpc([pairs[0]])
q = list(generate_polygon_pairs())

batch_provider = BatchHTTPProvider(endpoint_uri=POLYGON_RPC)
resp = batch_provider.make_batch_request(json.dumps(q))
results = list(rpc_response_batch_to_results(resp))

print(results)


res = decode_abi(['uint256', 'uint256', 'uint256'], bytes.fromhex(results[0][2:]))

print('reserve0 amount', res[0])
print('reserve1 amount', res[1])







