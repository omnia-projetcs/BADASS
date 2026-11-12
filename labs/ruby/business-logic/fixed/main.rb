def run(value)
  return "DENIED" unless value.is_a?(String) && value.match?(/\A[0-9]+\z/)
  quantity = Integer(value, 10)
  return "DENIED" unless (1..100).cover?(quantity)
  (1000 - quantity * 10).to_s
rescue ArgumentError
  "DENIED"
end
print run(ARGV.fetch(0))
