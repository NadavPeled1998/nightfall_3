from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from .find_elements import *
from .metamask import *
from decimal import Decimal

def loginNightfallWallet(driver, findElements, metamaskTab, nightfallTab, walletURL):
    driver.switch_to.window(nightfallTab)
    driver.get(walletURL)
    findElements.element_exist_xpath('(//*[local-name()="svg"])[2]').click() # nightfall Metamask button
    sleep(3)

    ## Connect Account to network
    driver.switch_to.window(metamaskTab)
    driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/popup.html#')
    nextButton = findElements.element_exist_xpath('//button[text()="Next"]') # Select new account
    if nextButton:
        nextButton.click()
        findElements.element_exist_xpath('//button[text()="Connect"]').click() # Connect

    driver.switch_to.window(nightfallTab)
    cancelButton = findElements.element_exist_xpath('//button[text()="Cancel"]')
    if cancelButton:
      cancelButton.click()
    sleep(1)
    findElements.element_exist_xpath('(//*[local-name()="svg"])[2]').click() # nightfall Metamask button
    sleep(1)
    findElements.element_exist_xpath('//button[text()="New"]').click() # New Mnemonic
    sleep(1)
    findElements.element_exist_xpath('//button[text()="Submit"]').click() # Submit Mnemonic

def logoutNightfallWallet(driver, findElements, nightfallTab):
    driver.switch_to.window(nightfallTab)
    findElements.element_exist_xpath('//button[text()="Logout"]').click() # Cancel

def submitTxWallet(txParams, findElements, driver, metamaskTab, nightfallTab, cancel=0):
    findElements.element_exist_xpath('//*[@title="' + txParams['tokenAddress'] + '"]').click() # Select token
    txType = txParams["txType"]
    if txParams["txType"] == "Instant-withdraw":
        txType="Withdraw"

    transactionButtonEn = findElements.element_exist_xpath('//button[text()="' + txType + '"]') # Transaction
    if transactionButtonEn.get_attribute("disabled"):
      findElements.element_exist_xpath('//*[@title="' + txParams['tokenAddress'] + '"]').click() # Select token
    transactionButtonEn.click()

    if txParams["tokenType"].lower() != "erc721":
      findElements.element_exist_xpath('//*[@id="amount"]').send_keys(txParams['amount']) # Amount

    if txParams["tokenType"].lower() == "erc721":
      sleep(5)
      findElements.element_exist_xpath('//*[@id="token-id"]').click()

    findElements.element_exist_xpath('//*[@id="fee"]').send_keys(txParams['fee']) # Fee
    if txParams["txType"] == "Transfer":
      findElements.element_exist_xpath('//*[@id="destination address"]').send_keys(txParams['compressedPkd']) # compressedPkd
    elif txParams["txType"] == "Withdraw" or txParams["txType"] == "Instant-withdraw":
      findElements.element_exist_xpath('//*[@id="destination address"]').send_keys(txParams['ethereumAddress']) # Ethereum Address

    if txParams["txType"] == "Instant-withdraw":
      findElements.element_exist_xpath('(//div[contains(@class, "ui checkbox")])[1]').click() # Instant Withdraw
      findElements.element_exist_xpath('//*[@id="instant withdraw fee"]').send_keys(txParams['instantWithdrawFee']) # Fee


    testTokenType = findElements.element_exist_xpath('//*[@id="token-type"]').get_attribute("value") # Read Token Type
    testTokenAddress = findElements.element_exist_xpath('//*[@id="token-address"]').get_attribute("value") # Read Token Address
    assert(testTokenType.lower() == txParams['tokenType'].lower())
    assert(testTokenAddress.lower() == txParams['tokenAddress'].lower())
    if cancel == 1:
      findElements.element_exist_xpath('//button[text()="Cancel"]').click() # Cancel
      return

    findElements.element_exist_xpath('//button[text()="Submit"]').click() # Submit
    driver.switch_to.window(metamaskTab)

    stop=0
    if txParams['tokenType'] == "erc20" and txType == "Withdraw":
       stop=0
    # Approve/sign tokens
    signTransactionMetamask(driver, findElements, stop) # sign transaction
    driver.switch_to.window(nightfallTab)

def tokenRefresh(txParams,findElements):
    findElements.element_exist_xpath('//*[@title="' + txParams['tokenAddress'] + '"]').click() # Select token
    transactionButtonEn = findElements.element_exist_xpath('//button[text()="Deposit"]') # Transaction
    if transactionButtonEn.get_attribute("disabled"):
      findElements.element_exist_xpath('//*[@title="' + txParams['tokenAddress'] + '"]').click() # Select token

def getNightfallBalance(findElements, tokenInfo):
  niter=0
  while True:
    l1BalanceId="l1 balance" + tokenInfo["tokenAddress"]
    l2BalanceId="l2 balance" + tokenInfo["tokenAddress"]
    pendingDepositId="pending deposit" + tokenInfo["tokenAddress"]
    pendingTransferredOutId="pending transferred out" + tokenInfo["tokenAddress"]
    l1Balance = findElements.element_exist_xpath('//*[@id="' +l1BalanceId + '"]').get_attribute("title")
    l2Balance = findElements.element_exist_xpath('//*[@id="' +l2BalanceId + '"]').get_attribute("title")
    pendingDeposit = findElements.element_exist_xpath('//*[@id="' +pendingDepositId + '"]').get_attribute("title")
    pendingTransferredOut = findElements.element_exist_xpath('//*[@id="' +pendingTransferredOutId + '"]').get_attribute("title")
    try:
      return Decimal(l1Balance), Decimal(l2Balance), Decimal(pendingDeposit), Decimal(pendingTransferredOut)
    except:
      niter+=1
      if niter == 10:
        raise ValueError("Unexpected balance")
    sleep(3)

def addTokenNightfallWallet(driver, findElements, tokenInfo):
  findElements.element_exist_xpath('//button[text()="Add Token"]').click() # Add Token
  sleep(3)
  findElements.element_exist_xpath('//*[@id="Token Name"]').send_keys(tokenInfo['tokenName']) # Set Token Name
  sleep(3)
  findElements.element_exist_xpath('//*[@id="Token Address"]').send_keys(tokenInfo['tokenAddress']) # Set Address
  sleep(3)
  findElements.element_exist_xpath('//button[text()="Submit"]').click() # Submit

def addAndCheckTokenNightfallWallet(driver, findElements, tokenInfo, erc1155TokenId=None):
  findElements.element_exist_xpath('//button[text()="Add Token"]').click() # Add Token
  findElements.element_exist_xpath('//*[@id="Token Name"]').send_keys(tokenInfo['tokenName']) # Set Token Name
  sleep(3)
  if not erc1155TokenId:
    findElements.element_exist_xpath('//*[@id="Token Address"]').send_keys(tokenInfo['tokenAddress']) # Set Address
  else:
    testTokenAddress = findElements.element_exist_xpath('//*[@id="Token Address"]').get_attribute("value") # Read address
    assert(testTokenAddress.lower() == tokenInfo['tokenAddress'].lower())
  sleep(3)
  testTokenType = findElements.element_exist_xpath('//*[@id="Token Type"]').get_attribute("value") # Read Token Type
  if tokenInfo['tokenType'] != '':
    assert(testTokenType.lower() == tokenInfo['tokenType'].lower())

  if erc1155TokenId:
     findElements.element_exist_xpath('//*[@id="Token Id"]').send_keys(erc1155TokenId) # Set Address

  findElements.element_exist_xpath('//button[text()="Submit"]').click() # Submit

def removeTokenNightfallWallet(driver, findElements, tokenInfo, erc1155TokenId=None):
  if erc1155TokenId:
     sleep(3)
     findElements.element_exist_xpath('//*[@title="' + tokenInfo['tokenAddress'].lower() + '"]').click() # Select token
     sleep(1)
     findElements.element_exist_xpath('//*[@title="' + tokenInfo['tokenAddress'].lower() + '"]').click() # Select token
  findElements.element_exist_xpath('//button[@id="wallet-info-cell-remove-token"]').click() # Remove Token
  if not erc1155TokenId:
    findElements.element_exist_xpath('//*[@title="' + tokenInfo['tokenAddress'].lower() + '"]').click() # Select token
  else:
    findElements.element_exist_xpath('//*[@id="token type' + tokenInfo['tokenAddress'].lower() + erc1155TokenId +'"]').click() # Select token
