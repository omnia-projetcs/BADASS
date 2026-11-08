def run(value)
  size = Integer(value)
  raise ArgumentError if size < 0
  data = Array.new(size, 0)
  data.length.to_s
end
print run(ARGV.fetch(0))
