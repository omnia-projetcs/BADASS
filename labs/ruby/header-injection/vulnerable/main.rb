def run(value)
  "X-User: " + value + "\r\n\r\nBODY"
end
print run(ARGV.fetch(0))
