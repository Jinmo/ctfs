const Web3 = require('web3');

// parameters from server and the given binary
const host = 'public-node',
    contract = `0x3D032833714CAd4baC4Dde9345F13cEB4CBAE293`,
    mine = `0x63e16616209f7ddaa54ed750d2c0efea8f6e1930`,
    gasPrice = `0x430E23400`;

const web3 = new Web3(new Web3.providers.HttpProvider("http://" + host + ":8545"));

const hashed_data = `6a696e6d6f3132336a696e6d6f3132336a696e6d6f3132336a696e6d6f313233`,
    hash = `c3eb7dd7e8db5217fbced80f5e65bbfed8609e3e670e5cb554994af8d7ee9463`,
    secret = `221f2af61b5ece33daa443a3413d662e620f61abb59a025b10eaedf781baecd7`;

// input for the contract
const setHash = `0x979ea13b` + secret + hash,
    verifyHash = `0x09AF8FFE` + hashed_data;

// storage index that contains the random data
const storageAddr = '0x3'

const log = x => x.then(x => console.log(x)).catch(x => {
    console.log('Rej: ' + x)
})

const printLatestTransactions = () => web3.eth.getBlockNumber().then(x => {
    for (var i = 0; i < 100; i++)
        web3.eth.getBlock(x--).then(tr => {
            for (a of tr.transactions) {
                web3.eth.getTransaction(a).then(trs => {
                    console.log(tr.timestamp.toString(16), trs.input)
                })
            }
        })
})

web3.eth.sendTransaction({
    to: contract,
    from: mine,
    gasPrice: gasPrice,
    data: data // set storage index 3 given secret
}).then(x => {
    console.log('letsgetit')
    log(web3.eth.getStorageAt(contract, storageAddr)) // used when debugging

    web3.eth.sendTransaction({
        to: contract,
        from: mine,
        gasPrice: gasPrice,
        // and just verify with my payload
        data: verifyHash
    }).then(x => setTimeout(printLatestTransactions, 10000))
})