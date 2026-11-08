'use strict';
// Checkout recomputes the price from the trusted server catalog.
const fs = require('node:fs');
const PRICES = Object.freeze({book: 120, lamp: 250});

function quote(request, prices = PRICES, balance = 1000) {
    if (!request || typeof request !== 'object' || Array.isArray(request)
        || typeof request.product !== 'string') return {status: 400};
    const {product, quantity, unit_price: suppliedPrice} = request;
    if (!Number.isInteger(quantity) || quantity < 1 || quantity > 5
        || !Number.isInteger(suppliedPrice) || suppliedPrice < 0 || suppliedPrice > 10000) return {status: 400};
    if (!Object.prototype.hasOwnProperty.call(prices, product)) return {status: 404};
    // The client quote is informational; only the server catalog sets the charge.
    const unitPrice = prices[product];
    const total = quantity * unitPrice;
    if (total > balance) return {status: 402};
    return {status: 201, receipt: {product, quantity, unit_price: unitPrice,
        total, remaining: balance - total}};
}

function run(request) {
    const result = quote(request);
    if (result.status !== 201) return result;
    const receipt = result.receipt;
    fs.writeFileSync('order.json', JSON.stringify(receipt) + '\n', 'utf8');
    return {status: 201, total: receipt.total, remaining: receipt.remaining};
}

module.exports = {run, quote};
if (require.main === module) {
    let request;
    try { request = JSON.parse(process.argv[2]); }
    catch { process.stdout.write(JSON.stringify({status: 400})); process.exit(0); }
    process.stdout.write(JSON.stringify(run(request)));
}
