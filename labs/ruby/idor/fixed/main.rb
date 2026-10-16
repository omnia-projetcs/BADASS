def run(value)
  records = {"alice" => "ALICE_DATA", "bob" => "BOB_PRIVATE"}
  return "NOT_FOUND" unless records.key?(value)
  return "DENIED" unless value == "alice"
  records[value]
end
print run(ARGV.fetch(0))
