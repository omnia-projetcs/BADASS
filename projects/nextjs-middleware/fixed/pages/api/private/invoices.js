export default function handler(req, res) {
  const expected = process.env.LAB_SESSION_TOKEN;
  const supplied = req.cookies?.['lab-session'];
  if (typeof expected !== 'string' || !expected || typeof supplied !== 'string' || supplied !== expected) {
    res.status(401).json({ error: 'Unauthorized' });
    return;
  }
  res.status(200).json({ invoices: [{ id: 'INV-001', customer: 'LAB_PRIVATE_CUSTOMER', amount: 10000 }] });
}
