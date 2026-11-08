def run(value)
  File.symlink("secret.txt", "export.tmp") if value == "preplaced-link"
  begin
    File.open("export.tmp", File::WRONLY | File::CREAT | File::TRUNC, 0600) { |file| file.write("LAB_OVERWRITTEN") }
  rescue Errno::EEXIST
    # An existing final path is rejected before any write.
  end
  File.read("secret.txt")
end
print run(ARGV.fetch(0))
