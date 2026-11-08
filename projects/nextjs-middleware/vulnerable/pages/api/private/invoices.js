export default function handler(req, res) {
  res.status(200).json({ invoices: [{ id: 'INV-001', customer: 'LAB_PRIVATE_CUSTOMER', amount: 10000 }] });
}
