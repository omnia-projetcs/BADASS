# Ruby profile update merging all parsed JSON keys into the account hash.
require "json"

def run(raw)
  account = { "name" => "Alice", "role" => "user" }
  account.merge!(JSON.parse(raw))
  "#{account['name']}:#{account['role']}"
end

print run(ARGV.fetch(0))
