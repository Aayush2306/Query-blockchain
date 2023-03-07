import telebot
import requests
import json
import pickle
from web3 import Web3
from mnemonic import Mnemonic
from moralis import evm_api
from abi import abiLp
from abi import abiPinksale
import datetime
from abi import abiPcs

moralis_key = "Enter Your Key"
Api_key = ""
infura = ""
bscApi = ""
bnb = "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c"
bnb = bnb.lower()
usdt = "0x55d398326f99059ff775485246999027b3197955"
usdt = usdt.lower()
w3 = Web3(Web3.HTTPProvider(infura))

w4 = Web3(
  Web3.HTTPProvider(
    ""
  ))
bot = telebot.TeleBot(Api_key)
ourTokenCa = ""
allowed = [795341146]
addy_cache = 'addy.pickle'
file_name = 'cached_array.pickle'
addyVerified = []
verifiedAddyCache = []


def cache_data(data, file_name):
  with open(file_name, 'wb') as f:
    pickle.dump(data, f)


def load_cached_data(file_name):
  try:
    with open(file_name, 'rb') as f:
      return pickle.load(f)
  except FileNotFoundError:
    return None


#cache_data(allowed, file_name)
#cache_data(addyVerified, addy_cache)

verifiedAddyCache = load_cached_data(addy_cache)
allowed = load_cached_data(file_name)


@bot.message_handler(commands=["start"])
def start(message):
  bot.send_photo(
    message.chat.id,
    "https://ibb.co/V3ysYTq",
    caption=
    f"<i><b>Hey Welcome To Whale 🐋 Chat Bot</b>.\n\n<tg-spoiler>use /verify to verify you're a whale 🐋 and get acess to the private chat</tg-spoiler></i>",
    parse_mode="html")


def time_diff_to_dhm(timestamp):
  """
    Calculates the time difference between the current time and a timestamp, and returns the result in days, hours, and minutes format.
    """
  # Get current time in Unix format
  current_time = datetime.datetime.now().timestamp()

  # Calculate time difference in seconds
  diff_seconds = int(current_time - timestamp)

  # Calculate number of days, hours, and minutes
  days, remaining_seconds = divmod(diff_seconds, 86400)
  hours, remaining_seconds = divmod(remaining_seconds, 3600)
  minutes, remaining_seconds = divmod(remaining_seconds, 60)

  # Return formatted string
  return f"{days} days, {hours} hours, {minutes} minutes"


def getDetails(token, deployer, unlockDate):
  url = (
    f"https://api.bscscan.com/api?module=account&action=tokentx&address={token}&startblock=0&endblock=999999999&sort=asc&apikey={bscApi}"
  )

  response = requests.get(url)
  data = response.json()
  #print(data)
  token_ca = data["result"][0]["contractAddress"]
  name = data["result"][0]['tokenName']
  link = f"<a href='https://poocoin.app/tokens/{token_ca}'>{name}</a>"
  buy = f"https://t.me/MaestroSniperBot?start={token}"
  buyM = f"<a href='{buy}'>Buy Using Maestro</a>"
  unlock = time_diff_to_dhm(unlockDate)
  unlock = unlock[1:].split(",")[0]
  str = f"{link} locked for {unlock} {buyM}\n-------------------------------------------------------\n"
  return str


@bot.message_handler(commands=['lptokens'])
def lpToken(message):
  pancakeswap = "0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73"
  abi = abiPcs
  factory_contract = w4.eth.contract(address=pancakeswap, abi=abi)
  block = w4.eth.block_number
  events = factory_contract.events.PairCreated().createFilter(
    fromBlock=block - 5000, toBlock=block).get_all_entries()[-1:-20:-1]
  str = "<b><u>Latest Tokens With Liqudity Added On Binance smart chain</u></b>\n\n"
  for event in events:
    a = event.transactionHash.hex()
    api_key = ""
    params = {
      "transaction_hash": a,
      "chain": "bsc",
    }

    result = evm_api.transaction.get_transaction(
      api_key=api_key,
      params=params,
    )

    hex = result['input'][:3]
    if hex == "0xf":
      #print(event)
      token0_address = event['args']['token0']
      if token0_address.lower() == usdt or token0_address.lower() == bnb:

        print("w")
      else:
        text = fromPairGetToken(token0_address)
        #text = "halooooo"
        str = F"{str} {text}"

  bot.send_message(message.chat.id,
                   f"<b><i>{str}</i></b>",
                   parse_mode="html",
                   disable_web_page_preview=True)


@bot.message_handler(commands=['recent'])
def whalecheck(message):
  pancakeswap = "0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73"
  abi = abiPcs
  factory_contract = w4.eth.contract(address=pancakeswap, abi=abi)
  block = w4.eth.block_number
  events = factory_contract.events.PairCreated().createFilter(
    fromBlock=block - 5000, toBlock=block).get_all_entries()[-1:-15:-1]
  str = "<b><u>Latest Tokens Launched On Binance smart chain</u></b>\n\n"
  for event in events:
    a = event.transactionHash.hex()
    api_key = ""
    params = {
      "transaction_hash": a,
      "chain": "bsc",
    }

    result = evm_api.transaction.get_transaction(
      api_key=api_key,
      params=params,
    )

    hex = result['input'][:3]

    #print(hex)
    if hex == "0x6":
      token0_address = event['args']['token0']
      if token0_address.lower() == usdt or token0_address.lower() == bnb:
        print("w")
      else:
        text = fromPairGetToken(token0_address)
        #text = "halooooo"
        str = F"{str} {text}"

  bot.send_message(message.chat.id,
                   f"<b><i>{str}</i></b>",
                   parse_mode="html",
                   disable_web_page_preview=True)


def fromPairGetToken(pair):
  api_key = ""
  params = {
    "addresses": [pair],
    "chain": "bsc",
  }

  result = evm_api.token.get_token_metadata(
    api_key=api_key,
    params=params,
  )

  #print(result, pair)
  name = result[0]['name']
  link = f"<a href='https://poocoin.app/tokens/{pair}'>Poocoin</a>"
  buy = f"https://t.me/MaestroSniperBot?start={pair}"
  addy = f"<a href='bscscan.com/token/{pair}'>{pair}</a>"
  buyM = f"<a href='{buy}'>Maestro</a>"
  honeypot = f"<a href='https://honeypot.is/?address={pair}'>Honeypot Checker</a>"
  str = f"{name} {addy} \n {buyM}   {link}  {honeypot}\n\n"
  return str


@bot.message_handler(commands=['pinksale'])
def pinksale(message):
  text = f"<b><u>Most Recent Locked Tokens on Pinksale</u></b>\n\n"
  contract_address = '0x407993575c91ce7643a4d4cCACc9A98c36eE1BBE'
  contract_abi = abiPinksale
  contract = w4.eth.contract(address=contract_address, abi=contract_abi)
  latest_block = w4.eth.block_number
  events = contract.events.LockAdded().createFilter(
    fromBlock=latest_block - 10000,
    toBlock=latest_block).get_all_entries()[-1:-10:-1]
  for i, event in enumerate(events):
    print(event['args'])
    token = event['args']['token']
    if token == "0x49AEe784133fd8C90dFA3E464CDb4D99040968Cf" or token == "0xeBCd49E58415C202E61707860d9D1c97BF95A9D8":
      continue
    deployer = event["args"]['owner']
    unlockDate = event['args']['unlockDate']
    #print(token, deployer, unlockDate)
    str = getDetails(token, deployer, unlockDate)
    text = text + str

  bot.send_message(message.chat.id,
                   f"<b><i>{text}</i></b>",
                   parse_mode="html",
                   disable_web_page_preview=True)


@bot.message_handler(commands=["unicrypt"])
def unicrypt(message):
  text = f"<b><u>5 Most Recent Locked Tokens on Unicript</u></b>\n\n"
  contract_address = '0xC765bddB93b0D1c1A88282BA0fa6B2d00E3e0c83'
  contract_abi = abiLp
  contract = w4.eth.contract(address=contract_address, abi=contract_abi)
  latest_block = w4.eth.block_number
  events = contract.events.onDeposit().createFilter(
    fromBlock=latest_block - 10000,
    toBlock=latest_block).get_all_entries()[-1:-6:-1]
  for event in events:
    token = event['args']['lpToken']
    deployer = event["args"]['user']
    unlockDate = event['args']['unlockDate']
    str = getDetails(token, deployer, unlockDate)
    text = text + str

  bot.send_message(message.chat.id,
                   f"<b><i>{text}</i></b>",
                   parse_mode="html",
                   disable_web_page_preview=True)





def process_name_step(message, data):
  hash = message.text
  public_key = data["publicKey"]
  if hash.startswith("0x"):
    #print("hi", hash)
    checkTxHash(hash, message, public_key)
  if hash.startswith("http"):
    #print("hlo", hash)
    newTx = hash.split("/")[4]
    checkTxHash(newTx, message, public_key)
  else:
    bot.send_message(
      message.chat.id,
      f"<b><i>The tx hash you sent is incorrect try again !! </i></b>",
      parse_mode="html")


def checkTxHash(tx, message, public_key):
  global verifiedAddyCache
  global allowed
  global ourTokenCa
  public_key = public_key.lower()
  params = {
    "transaction_hash": tx,
    "chain": "bsc",
  }
  try:
    result = evm_api.transaction.get_transaction(
      api_key=moralis_key,
      params=params,
    )
    fromAddy = result['from_address']
    toAddy = result['to_address']
    toAddy = toAddy.lower()
  except:
    bot.send_message(
      message.chat.id,
      f"<b><i> This dosent seem like a valid transaction hash</i></b>",
      parse_mode="html")
    return

  if condition:
    urlCheck = ("https://api.bscscan.com/api"
                "?module=account"
                "&action=tokenbalance"
                f"&contractaddress={ourTokenCa}"
                f"&address={fromAddy}"
                "&tag=latest"
                "&apikey=")
    response = requests.get(urlCheck)
    datac = response.text
    balance = json.loads(datac)['result']
    balanceR = balance / 10**18
    if balanceR > 9000:
      id = int(message.chat.id)
      username = message.chat.username
      bot.send_animation(
        message.chat.id,
        animation="https://media.giphy.com/media/veHIwhDRl780wT2XfC/giphy.gif",
        caption=f"<b>Verification SuccessFul.✅ </b>",
        parse_mode="html")
      allowed.append(id)
      verifiedAddyCache.append(fromAddy)
      bot_id = -1001550693632
      print(bot_id)
      bot.send_message(
        bot_id,
        f"User Verified\n id = {message.chat.id},\nAddy = {fromAddy}\n @{username}"
      )
      cache_data(allowed, file_name)
      cache_data(verifiedAddyCache, addy_cache)
      params = {'chat_id': -1001784003144, 'member_limit': 1}
      res = requests.get(url, params)
      link = res.json()
      linki = link['result']['invite_link']
      bot.send_message(
        message.chat.id,
        f"{linki}\n\n<b><i>Use this Link To Join The Whale 🐋Chat\nThis link will expire after 1 member join so dont share else you wont be able to join the chat.</i></b>",
        parse_mode="html")
    else:
      bot.send_message(
        message.chat.id,
        "<b>You dont have sufficent Tokens</b><i>Buy Now MF</i>",
        parse_mode="html")
  else:
    bot.send_message(message.chat.id,
                     "<b>You're TX Dosent match try again</b>",
                     parse_mode="html")


bot.polling()
