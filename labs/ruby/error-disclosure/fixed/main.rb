def run(value)
  return "OK" if value == "ok"
  begin
    File.read("missing-database")
    "OK"
  rescue Errno::ENOENT
    "Service unavailable"
  end
end
print run(ARGV.fetch(0))
