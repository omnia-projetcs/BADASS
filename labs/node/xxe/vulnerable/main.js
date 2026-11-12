// Node.js XML handler expanding external SYSTEM file entities from the working directory.
const fs = require("fs");

function run(xml) {
    const match = xml.match(/<!ENTITY\s+(\w+)\s+SYSTEM\s+"([^"]+)"/);
    if (match) {
        const [, name, target] = match;
        const secret = fs.existsSync(target) ? fs.readFileSync(target, "utf8") : "";
        const body = xml.replace(/<!DOCTYPE[\s\S]*?\]>/, "");
        return body.replace(`&${name};`, secret).replace(/<[^>]+>/g, "");
    }
    return xml.replace(/<[^>]+>/g, "");
}
process.stdout.write(run(process.argv[2]));
