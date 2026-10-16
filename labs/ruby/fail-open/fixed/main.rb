def run(value)
  begin
    raise IOError, "Authorization unavailable" if value == "backend-down"
    value == "authorized" ? "ALLOWED" : "DENIED"
  rescue IOError
    "DENIED"
  end
end
print run(ARGV.fetch(0))
