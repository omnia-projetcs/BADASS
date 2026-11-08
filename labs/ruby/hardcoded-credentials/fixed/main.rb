def run(value)
  expected = ENV["BADASS_ADMIN_PASSWORD"]
  expected && !expected.empty? && value == expected ? "ADMIN" : "DENIED"
end
print run(ARGV.fetch(0))
