import web3
from web3.middleware import geth_poa_middleware
import time
import requests
import json
from time import sleep
import numpy as np

def swap(node, account_address, pvt_key, contract_address, contract_abi, action_type, amount_in):
    #load USDC and WETH contracts. Those are the tokens we are going to use.
    weth_addr = web3.Web3.toChecksumAddress('0x7ceb23fd6bc0add59e62ac25578270cff1b9f619')
    usdc_addr = web3.Web3.toChecksumAddress('0x2791bca1f2de4661ed88a30c99a7a9449aa84174')
    
    #connect to polygon node
    w3 = web3.Web3(web3.Web3.HTTPProvider(node))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    usdc_abi = '''[{"inputs":[{"internalType":"address","name":"childChainManager","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"userAddress","type":"address"},{"indexed":false,"internalType":"address payable","name":"relayerAddress","type":"address"},{"indexed":false,"internalType":"bytes","name":"functionSignature","type":"bytes"}],"name":"MetaTransactionExecuted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"previousAdminRole","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"newAdminRole","type":"bytes32"}],"name":"RoleAdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleGranted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleRevoked","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"CHILD_CHAIN_ID","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"CHILD_CHAIN_ID_BYTES","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"DEFAULT_ADMIN_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"DEPOSITOR_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"ERC712_VERSION","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"ROOT_CHAIN_ID","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"ROOT_CHAIN_ID_BYTES","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"bytes","name":"depositData","type":"bytes"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"userAddress","type":"address"},{"internalType":"bytes","name":"functionSignature","type":"bytes"},{"internalType":"bytes32","name":"sigR","type":"bytes32"},{"internalType":"bytes32","name":"sigS","type":"bytes32"},{"internalType":"uint8","name":"sigV","type":"uint8"}],"name":"executeMetaTransaction","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"getChainId","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"getDomainSeperator","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getNonce","outputs":[{"internalType":"uint256","name":"nonce","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleAdmin","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"getRoleMember","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleMemberCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"grantRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"hasRole","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"renounceRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"revokeRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]'''
    usdc_contract = w3.eth.contract(usdc_addr, abi=usdc_abi)
    weth_abi = '''[{"inputs":[{"internalType":"address","name":"childChainManager","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"userAddress","type":"address"},{"indexed":false,"internalType":"address payable","name":"relayerAddress","type":"address"},{"indexed":false,"internalType":"bytes","name":"functionSignature","type":"bytes"}],"name":"MetaTransactionExecuted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"previousAdminRole","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"newAdminRole","type":"bytes32"}],"name":"RoleAdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleGranted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleRevoked","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"CHILD_CHAIN_ID","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"CHILD_CHAIN_ID_BYTES","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"DEFAULT_ADMIN_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"DEPOSITOR_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"ERC712_VERSION","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"ROOT_CHAIN_ID","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"ROOT_CHAIN_ID_BYTES","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"bytes","name":"depositData","type":"bytes"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"userAddress","type":"address"},{"internalType":"bytes","name":"functionSignature","type":"bytes"},{"internalType":"bytes32","name":"sigR","type":"bytes32"},{"internalType":"bytes32","name":"sigS","type":"bytes32"},{"internalType":"uint8","name":"sigV","type":"uint8"}],"name":"executeMetaTransaction","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"getChainId","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"getDomainSeperator","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getNonce","outputs":[{"internalType":"uint256","name":"nonce","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleAdmin","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"getRoleMember","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleMemberCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"grantRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"hasRole","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"renounceRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"revokeRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]'''
    weth_contract = w3.eth.contract(weth_addr, abi=weth_abi)


    #This is the smart contract we will interact with to buy or sell the tokens.
    contract_addr = web3.Web3.toChecksumAddress(contract_address.lower())
    contract = w3.eth.contract(contract_addr, abi=contract_abi)

    #set a correct gas price. This line of code could be surely optimized.
    gasPrice = w3.toWei(330, 'gwei')


    #===BE SURE YOU APPROVED BOTH TOKENS CONTRACT.

    nonce = w3.eth.getTransactionCount(account_address)

    tx = usdc_contract.functions.approve(contract_address, 1000000000000).buildTransaction({
        'from': account_address, 
        'nonce': nonce
        })
        
    signed_tx = w3.eth.account.signTransaction(tx, pvt_key)
    #tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    #tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)


    nonce = w3.eth.getTransactionCount(account_address)
    
    tx = weth_contract.functions.approve(contract_address, 1000000000000000000000000).buildTransaction({
        'from': account_address, 
        'nonce': nonce
        })
        
    signed_tx = w3.eth.account.signTransaction(tx, pvt_key)
    #tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    #tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    if action_type == True:
        #Buy WETH
        amount_usdc = int(amount_in*10**6)
        
        swap_path = [usdc_addr, weth_addr]
        amount_eth = contract.functions.getAmountsOut(amount_usdc, swap_path).call()[1]
        print(swap_path)

        #execute swap
        deadline = int(time.time() + 60)
        function = contract.functions.swapExactTokensForTokensSupportingFeeOnTransferTokens(
          amount_usdc,
          amount_eth,
          swap_path,
          account_address,
          deadline
        )
    
    if action_type == False:
        #Sell WETH
        amount_eth = int(amount_in*10**18)
        
        swap_path = [weth_addr, usdc_addr]
        amount_usdc = contract.functions.getAmountsOut(amount_eth, swap_path).call()[1]

        #execute swap
        deadline = int(time.time() + 60)
        function = contract.functions.swapExactTokensForTokensSupportingFeeOnTransferTokens(
          amount_eth,
          amount_usdc,
          swap_path,
          account_address,
          deadline
        )

    tx = function.buildTransaction({
        'from': account_address,
        'nonce': nonce,
        'gasPrice': gasPrice,
    })
        
    signed_tx = w3.eth.account.signTransaction(tx, pvt_key)
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    return amount_eth, amount_usdc

def entry_point():
    cumulative_volume = np.array([])
    price = np.array([])
    tvl = np.array([])
    
    w3 = web3.Web3(web3.Web3.HTTPProvider(node))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    current_block = w3.eth.getBlock('latest', full_transactions=True)['number']
    num_block = current_block-21060
    
    i = 0
    
    for k in range(13):
        block_to_use = num_block+i

        params = {
            "query":'{ liquidityPool(id: "0x45dda9cb7c25131df268515131f647d726f50608", block: {number: %s}) { tick cumulativeVolumeUSD totalValueLockedUSD inputTokenBalancesUSD inputTokenBalances } }'%str(block_to_use),
            "operationName": None,
            "variables": None,
            }
        
        url = 'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-polygon'
        
        while True:
            try:
                data = requests.post(url, data=json.dumps(params)).json()['data']['liquidityPool']
                cumulative_volume = np.append(cumulative_volume, float(data['cumulativeVolumeUSD']))
                #tvl = np.append(tvl, float(data['totalValueLockedUSD']))
                eth_price = 1/((1.0001 **int(data['tick']))* (10 ** -12))
                price = np.append(price, eth_price)
                break
            except Exception as e:
                sleep(0.5)
                continue
        i = i+1620
        
    price = price[1:]
    net_volume = cumulative_volume[1:] - cumulative_volume[:-1]

    ema_twelve = np.mean(price)
    mean_vol_twelve = np.mean(price)

    current_hourly_price = price[0]
    current_hourly_volume = net_volume[0]

    #if current price is under EMA12 and volume of last hour is above the last 12H mean value, we will trigger the buy signal

    if current_hourly_price < ema_twelve and current_hourly_volume > mean_vol_twelve:
        return True, current_hourly_price
    else:
        return True, current_hourly_price


def exit_point(purchase_price, stop_loss, take_profit):
    w3 = web3.Web3(web3.Web3.HTTPProvider(node))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    current_block = w3.eth.getBlock('latest', full_transactions=True)['number']

    params = {
        "query":'{ liquidityPool(id: "0x45dda9cb7c25131df268515131f647d726f50608", block: {number: %s}) { tick } }'%str(current_block),
        "operationName": None,
        "variables": None,
        }
    
    url = 'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-polygon'
    data = requests.post(url, data=json.dumps(params)).json()['data']['liquidityPool']

    eth_price = 1/((1.0001 **int(data['tick']))* (10 ** -12))

    if (purchase_price+(purchase_price*(stop_loss/10))) > eth_price or (purchase_price+(purchase_price*(take_profit/10))) < eth_price:
        return True, eth_price
    else:
        return False, eth_price



#We are acting on polygon blockchain so we setup some starting setting
    
#These are chain-settings
node = 'https://polygon-rpc.com'

account_from = {
    'private_key': 'XXX',
    'address': web3.Web3.toChecksumAddress('XXX')
    }

contract_address = '0x0dc8e47a1196bcb590485ee8bf832c5c68a52f4b'
contract_abi = '''[{"inputs":[{"internalType":"address","name":"_bentoBox","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"bentoBox","outputs":[{"internalType":"contract IBentoBoxMinimal","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bytes","name":"route","type":"bytes"}],"name":"processRoute","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address payable","name":"transferValueTo","type":"address"},{"internalType":"uint256","name":"amountValueTransfer","type":"uint256"},{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bytes","name":"route","type":"bytes"}],"name":"transferValueAndprocessRoute","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"payable","type":"function"},{"stateMutability":"payable","type":"receive"}]'''

#trading settings
#starting_budget in USDC
amount_in = 20

#take profit and stop loss expressed in percentage
take_profit = 10
stop_loss = 10

#Entering into the main loop, while user want to run the bot it will keep running
print('Welcome to the AI Trading Bot developed by Astrid Network Team.\n\n')

while True:
    print('Looking for a good entry point...')

    while True:
        signal, purchase_price = entry_point()
        if signal == False:
        
            #if we don't find a good entry-point we wait 30 minutes more
            sleep(1800)
            continue
    
        if signal == True:
            action_type = True
            print('Entry-Point found. Optimal Time to buy WETH! Executing the transaction...')

            #buy WETH
            amount_eth, amount_usdc = swap(node, account_address, pvt_key, contract_address, contract_abi, action_type, amount_in)
            #amount of eth bought is 'amount_eth'
            print('Bought '+str(amount_eth)+' for '+str(amount_usdc))
            break

    #now check every minute if we get an exit-point
    while True:
        result, sold_price = exit_point(purchase_price, stop_loss, take_profit)

        if result == True:
            amount_in = amount_eth
            amount_eth, amount_in = swap(node, account_address, pvt_key, contract_address, contract_abi, action_type, amount_in)
            print('Sold '+str(amount_eth)+' for '+str(amount_eth*sold_price))
            break
        if result == False:
            sleep(60)
            continue
        
    print('\n\n\n')
        
