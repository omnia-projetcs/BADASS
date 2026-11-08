def run(value)
  quantity = Integer(value)
  return "DENIED" unless (1..100).cover?(quantity)
  (1000 - quantity * 10).to_s
end
print run(ARGV.fetch(0))
