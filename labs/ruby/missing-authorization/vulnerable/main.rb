def run(value)
  return "HEALTHY" if value == "health"
  role = "user"
  users = ["alice", "bob"]
  users.clear
  "USERS_DELETED"
end
print run(ARGV.fetch(0))
