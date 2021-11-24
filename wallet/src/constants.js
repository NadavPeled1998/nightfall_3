/* ignore unused exports */
const DEFAULT_NF_ADDRESS_INDEX = 0;
const DEFAULT_ENVIRONMENT = 'Docker';
const NF3_GITHUB_ISSUES_URL = 'https://github.com/EYBlockchain/nightfall_3/issues';
const DEFAULT_TOKEN_TYPE = 'ERC20';
const TOKEN_TYPE = {
  ERC20: 'ERC20',
  ERC721: 'ERC721',
  ERC1155: 'ERC1155',
};
const DEFAULT_TOKEN_ADDRESS = {
  ERC20: '0xe1b7B854F19A2CEBF96B433ba30050D8890618ab'.toLowerCase(),
  ERC721: '0xf05e9fb485502e5a93990c714560b7ce654173c3'.toLowerCase(),
  ERC1155: '0xb5acbe9a0f1f8b98f3fc04471f7fe5d2c222cb44'.toLowerCase(),
};

const DEFAULT_DEPOSIT_AMOUNT = 0;
const DEFAULT_DEPOSIT_FEE = 10;
const DEFAULT_INSTANT_WITHDRAW_FEE = 100;
const DEFAULT_TOKEN_ID = {
  ERC20: [0],
  ERC721: [
    '0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
    '0x1111111111111111111111111111111111111111',
    '0x2222222222222222222222222222222222222222',
  ],
  ERC1155: [
    '0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
    '0x3333333333333333333333333333333333333333',
    '0x4444444444444444444444444444444444444444',
  ],
};

const TX_TYPES = {
  DEPOSIT: 'deposit',
  TRANSFER: 'transfer',
  WITHDRAW: 'withdraw',
  INSTANT_WITHDRAW: 'instant-withdraw',
};

const METAMASK_MESSAGE =
  'This signature is required to unlock your Nightfall account. Sign this message only if you are in a trusted application.';

const TRANSACTION_MAX_RETRIES = 10;
const TRANSACTION_RETRY_PERIOD = 10000; // 10s

export {
  DEFAULT_NF_ADDRESS_INDEX,
  DEFAULT_ENVIRONMENT,
  NF3_GITHUB_ISSUES_URL,
  DEFAULT_TOKEN_TYPE,
  DEFAULT_TOKEN_ADDRESS,
  DEFAULT_DEPOSIT_FEE,
  DEFAULT_INSTANT_WITHDRAW_FEE,
  DEFAULT_DEPOSIT_AMOUNT,
  DEFAULT_TOKEN_ID,
  TOKEN_TYPE,
  TX_TYPES,
  METAMASK_MESSAGE,
  TRANSACTION_MAX_RETRIES,
  TRANSACTION_RETRY_PERIOD,
};
