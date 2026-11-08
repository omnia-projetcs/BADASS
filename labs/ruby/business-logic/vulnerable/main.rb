def run(value)
  quantity = Integer(value)
  (1000 - quantity * 10).to_s
end
print run(ARGV.fetch(0))
