def run(value)
  File.open("stored-secret", File::WRONLY | File::CREAT | File::EXCL, 0600) do |file|
    file.write(value == "public" ? "PUBLIC" : "LAB_SECRET")
    file.chmod(0644)
    return format("%04o", file.stat.mode & 0777)
  end
end
print run(ARGV.fetch(0))
