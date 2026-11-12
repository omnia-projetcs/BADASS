def run(value)
  return "DENIED" unless value.is_a?(String) && value.match?(/\A[0-9]+\z/)
  size = Integer(value, 10)
  return "DENIED" if size < 0 || size > 100
  data = Array.new(size, 0)
  data.length.to_s
rescue ArgumentError
  "DENIED"
end
print run(ARGV.fetch(0))
