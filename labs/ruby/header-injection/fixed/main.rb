def run(value)
  return "DENIED" if value.include?("\r") || value.include?("\n")
  "X-User: " + value + "\r\n\r\nBODY"
end
print run(ARGV.fetch(0))
