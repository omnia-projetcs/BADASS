def run(value)
  return "DENIED" unless ["/home", "/profile"].include?(value)
  "Location: " + value
end
print run(ARGV.fetch(0))
