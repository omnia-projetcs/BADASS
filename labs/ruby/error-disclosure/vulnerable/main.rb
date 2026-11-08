def run(value)
  return "OK" if value == "ok"
  begin
    File.read("missing-database")
    "OK"
  rescue Errno::ENOENT
    "db://admin:LAB_SECRET@database/internal"
  end
end
print run(ARGV.fetch(0))
