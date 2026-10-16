def run(value)
  records = {"alice" => "ALICE_DATA", "bob" => "BOB_PRIVATE"}
  return "NOT_FOUND" unless records.key?(value)
  records[value]
end
print run(ARGV.fetch(0))
