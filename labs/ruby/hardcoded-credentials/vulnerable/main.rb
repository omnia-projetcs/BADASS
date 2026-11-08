def run(value)
  expected = "BADASS_LAB_DEFAULT"
  expected && !expected.empty? && value == expected ? "ADMIN" : "DENIED"
end
print run(ARGV.fetch(0))
